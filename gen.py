#!/usr/bin/env python

import ConfigParser
import webbrowser

from twython import Twython

config = ConfigParser.ConfigParser()
config.read('settings.cfg')
app_key = config.get('auth', 'app_key')
app_secret = config.get('auth', 'app_secret')

# Auth
twitter = Twython(app_key, app_secret)
auth = twitter.get_authentication_tokens()

OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

# send user to auth['auth_url']
webbrowser.open(auth['auth_url'], new=2)

twitter = Twython(app_key, app_secret, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
pin = raw_input('Enter PIN from twitter: ')
final_step = twitter.get_authorized_tokens(pin)

OAUTH_TOKEN = final_step['oauth_token']
OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']

# Get timeline
twitter = Twython(app_key, app_secret, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
timeline = twitter.get_user_timeline()

for status in timeline:
    print status['text']