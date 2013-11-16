#!/usr/bin/env python

import ConfigParser
import webbrowser
import re
from collections import defaultdict

from twython import Twython

# get twitter api keys
config = ConfigParser.ConfigParser()
config.read('settings.cfg')
app_key = config.get('auth', 'app_key')
app_secret = config.get('auth', 'app_secret')

# Auth
twitter = Twython(app_key, app_secret)
auth = twitter.get_authentication_tokens()

OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

# send user to auth URL in a new tab
webbrowser.open(auth['auth_url'], new=2)

# final spet of auth - change for web app
twitter = Twython(app_key, app_secret, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
pin = raw_input('Enter PIN from twitter: ')
final_step = twitter.get_authorized_tokens(pin)

# TODO: Save these tokens for resuse
OAUTH_TOKEN = final_step['oauth_token']
OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']

# Get timeline
twitter = Twython(app_key, app_secret, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
timeline = twitter.get_user_timeline(count=200)

# start splitting the statuses
data = defaultdict(lambda: defaultdict(int)) # {pos: {word: count}}
ignore_pattern = re.compile(r'http|[@#][A-Za-z0-9]+')

for status in timeline:
    for pos, word in enumerate(status['text'].split()):
        if not bool(ignore_pattern.search(word)):
            data[pos][word] += 1

print data