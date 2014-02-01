#!/usr/bin/env python

import ConfigParser
import webbrowser
from collections import defaultdict
import random
import re

from twython import Twython
import flask


TOKEN_FILE = 'tokens.cfg'

class Generate(object):
    '''
    Generates a tweet, storing words in memory, using Markov bigrams.
    '''
    def __init__(self, statuses):
        self.words = self.get_words(statuses) # get a list of clean words
        self.num_words = len(self.words)
        self.tokens = defaultdict(list) # maps (w2, w2 -> [w3, w4]) for every pair w1, w2
        self.triples()
        
    def get_words(self, statuses):
        '''
        Returns words in given statuses without any @ mentions, or hashtags.
        '''
        words = []
        ignore_pattern = re.compile(r'http|[@#][_A-Za-z0-9]+|RT|MT')
        for status in statuses: # for each status
            for word in status.split(): # for each word
                if not bool(ignore_pattern.search(word)):
                    words.append(word)
        return words
    
    def triples(self):
        '''
        Builds the tokens dictionary. For each (w1, w2, w3), maps
        (w1, w2) -> w3.
        '''
        if self.num_words < 3: return
        for i in xrange(self.num_words - 2):
            key = (self.words[i], self.words[i + 1])
            next_word = self.words[i + 2]
            self.tokens[key].append(next_word)
    
    def generate(self, size=6):
        '''
        Generate a tweet of given word size.
        '''
        seed_num = random.randint(0, self.num_words - 3) # this will be w1
        w1, w2 = self.words[seed_num], self.words[seed_num + 1]
        gen_words = []
        
        for i in xrange(size):
            gen_words.append(w1) # add w1
            w1, w2 = w2, random.choice(self.tokens[(w1, w2)]) # get a random w3 from list mapped to by (w1, w2)
        gen_words.append(w2)
        return ' '.join(gen_words)


def get_tokens():
    '''
    Returns twitter authentication tokens for an acccount.
    '''
    config = ConfigParser.RawConfigParser()
    config.read(TOKEN_FILE)
    return config.get('OAUTH', 'OAUTH_TOKEN'), config.get('OAUTH', 'OAUTH_TOKEN_SECRET')

def load_keys():
    '''
    get twitter api keys from saved file
    '''
    pass

config = ConfigParser.RawConfigParser()
config.read('settings.cfg')
app_key = config.get('auth', 'app_key')
app_secret = config.get('auth', 'app_secret')

OAUTH_TOKEN, OAUTH_TOKEN_SECRET = '', ''

try:
   with open(TOKEN_FILE):
       OAUTH_TOKEN, OAUTH_TOKEN_SECRET = get_tokens()
except IOError:
    # could not get keys from file
    
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
statuses = [status['text'] for status in timeline]

g = Generate(statuses)

for i in range(10):
    print g.generate(size=random.randint(6, 10))
