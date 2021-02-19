import os
import json
import yaml
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from copy import copy

from html_templates import generate_posting_list

from craigslist import CraigslistForSale

# GLOBALS
CONFIG_FILENAME = "config.yaml"

with open(CONFIG_FILENAME, 'r') as config:
    config = yaml.safe_load(config)

with open(config['query_filename'], 'r') as queries_file:
    queries = yaml.safe_load(queries_file)

storage_filename = config['storage_filename']
saved_ids = set()
if os.path.exists(storage_filename):
    with open(storage_filename, 'r') as hist:
        historical = yaml.safe_load(hist)
        saved_ids = set(historical.keys())

found_posts = {}
for query in queries['queries']:
    sites = query['sites']
    category = query['category']
    filters = query['filters']

    # Crawl the craigslist
    for site in sites:
        CL_query = CraigslistForSale(site=site, category=category, filters=filters)
        found_posts.update({ result['id'] : result for result in CL_query.get_results() })

# fun set logic
post_ids = set(found_posts.keys())
old_ids = saved_ids & post_ids # posts which no longer appear in searches shouldn't be notified
new_ids = post_ids - old_ids

postings_to_notify = {post_id : found_posts[post_id] for post_id in new_ids}
postings_to_remind = {post_id : found_posts[post_id] for post_id in old_ids}

# Send an email
if postings_to_notify:
    receiver_email = queries['email']
    sender_email = config['sender_email']
    sender_password = config['sender_password'] # should really switch to google 2fa instead of plaintext passwords lol
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "New Craigslist postings detected!"
    message["From"] = sender_email
    message["To"] = receiver_email

    new_entries = generate_posting_list(postings_to_notify.values())
    old_entries = generate_posting_list(postings_to_remind.values())
    html_body = MIMEText(email_base_format.format(new_entries=new_entries, old_entries=old_entries), "html")
    message.attach(html_body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", smtp_port, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# save findings for future reference
# we could just save post ids but it's nice to have the links saved to a file somewhere
if found_posts:
    with open(storage_filename, 'w') as hist:
        yaml.dump(found_posts, hist)
 
