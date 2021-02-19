# cl scraper
it's a silly little script that searches craigslist for things that you want and then emails you

it's slow, it stores your email password in plaintext (make a burner email!), and it sometimes gets rate limited, but it works! I could make it faster, but a temporary fix is a permanent solution and who needs async requests and 2FA? Not me!

## setup
setup the venv
```
virtualenv -p python3 venv
source venv/bin/activate
```
install the craigslist library
```
pip install python-craigslist
```

pick an email. currently it's hard-coded to use gmail because I thought one day I might use their 2fa and avoid hard-coding a password. anyway, once the burner email is set up, you will need to [allow less secure apps](https://support.google.com/accounts/answer/6010255?hl=en) to access it before you can have python send emails from it. once that is done, stick the burner email info in `config.yaml` and whatever email you want to receive the notifications at in `queries.yaml` (beware, the emails usually go to spam at first, something about bare html, craigslist links, and weirdly named email accounts must be suspicious, who knew??)

## running the script
following setup, you can configure your query in `queries.yaml`. there are some examples there, if you want to know more about choosing a site, category, and filters you can look at the [python-craigslist documentation](https://pypi.org/project/python-craigslist/). then just run it:
```
python cl_scraper.py
```
it'll store any posts it finds in `notified_posts.yaml` and email you if it finds new ones. 

to make it a cron job, do `crontab -e` and paste this after your cron timings:
```
<absolute_path_to_cl_scraper_dir>/venv/bin/python <absolute_path_to_cl_scraper_dir>/cl_scraper.py
```
I would recommend calling this no more frequently than every 15 minutes, otherwise craigslist gets upset with you

