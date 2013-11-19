#!/usr/bin/env python

import ConfigParser
import webbrowser
import re
from collections import defaultdict
from collections import Counter
from random import randint

from twython import Twython


#-- Twitter Oauth --#
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

# final step of auth - change for web app
twitter = Twython(app_key, app_secret, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
pin = raw_input('Enter PIN from twitter: ')
final_step = twitter.get_authorized_tokens(pin)

# TODO: Save these tokens for resuse
OAUTH_TOKEN = final_step['oauth_token']
OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']


#-- Tweet data --#
# Get timeline
twitter = Twython(app_key, app_secret, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
timeline = twitter.get_user_timeline(count=200)

# start splitting the statuses
data = defaultdict(lambda: defaultdict(int)) # {pos: {word: count}}
word_count = [] # store the word count of each tweet

ignore_pattern = re.compile(r'http|[@#][A-Za-z0-9]+')

for status in timeline: # for each status
    words = 0
    for pos, word in enumerate(status['text'].split()): # for each word
        if not bool(ignore_pattern.search(word)):
            data[pos][word] += 1
            words += 1
    word_count.append(words)


#-- Generate tweet --#
# 5 most common tweet lengths
possible_tweet_lengths = Counter(word_count).most_common(5) # list of tuples

length = randint(possible_tweet_lengths[0][0], possible_tweet_lengths[-1],[0])

