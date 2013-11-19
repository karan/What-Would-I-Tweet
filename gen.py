#!/usr/bin/env python

import ConfigParser
import webbrowser
import re
from collections import defaultdict
from collections import Counter
from random import choice
import operator

from twython import Twython


TOKEN_FILE = 'tokens.cfg'

def get_tokens():
    config = ConfigParser.RawConfigParser()
    config.read(TOKEN_FILE)
    return config.get('OAUTH', 'OAUTH_TOKEN'), config.get('OAUTH', 'OAUTH_TOKEN_SECRET')

#-- Twitter Oauth --#
# get twitter api keys from saved file
config = ConfigParser.RawConfigParser()
config.read('settings.cfg')
app_key = config.get('auth', 'app_key')
app_secret = config.get('auth', 'app_secret')
OAUTH_TOKEN, OAUTH_TOKEN_SECRET = '', ''

try:
   with open(TOKEN_FILE):
       OAUTH_TOKEN, OAUTH_TOKEN_SECRET = get_tokens()
except IOError:
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
    
    # Save tokens
    config = ConfigParser.RawConfigParser()
    config.add_section('OAUTH')
    config.set('OAUTH', 'OAUTH_TOKEN_SECRET', OAUTH_TOKEN_SECRET)
    config.set('OAUTH', 'OAUTH_TOKEN', OAUTH_TOKEN)
    with open(TOKEN_FILE, 'wb') as configfile:
        config.write(configfile)


#-- Tweet data --#
# Get timeline
twitter = Twython(app_key, app_secret, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
timeline = twitter.get_user_timeline(count=200)

# start splitting the statuses
data = defaultdict(lambda: defaultdict(int)) # {pos: {word: count}}
word_count = [] # store the word count of each tweet

ignore_pattern = re.compile(r'http|[@#][_A-Za-z0-9]+|RT|MT')

for status in timeline: # for each status
    words = 0
    for pos, word in enumerate(status['text'].split()): # for each word
        if not bool(ignore_pattern.search(word)):
            data[pos][word] += 1
            words += 1
    word_count.append(words)

#-- Generate tweet --#
# 5 most common tweet lengths
possible_tweet_lengths = [c[0] for c in Counter(word_count).most_common(5)]

length = choice(possible_tweet_lengths)

chosen_words = []
for i in range(length):
    words = data[i] # get {word: count} for position
    chosen_words.append(
        sorted(words.iteritems(), key=operator.itemgetter(1), reverse=True)[0][0]
    )
    
print " ".join(chosen_words)