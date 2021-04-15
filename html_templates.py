from copy import copy

email_base_format = """\
<html>
  <body>
      <p>Found new craigslist entries:<br>
            {new_entries}
            And don't forget these:<br>
            {old_entries}
        </p>
    </body>
</html>"""

email_list_entry = """\
    <dl>
        <dt> <a href={url}> {title} - {price} - {location} </a>
    </dl><br>
"""

def generate_posting_list(postings):
    list_str = ""
    for e in postings:
        entry_str = copy(email_list_entry).format(url=e['url'], title=e['name'], price=e['price'], location=e['where'])
        list_str += entry_str
    return list_str

