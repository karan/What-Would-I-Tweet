#!/usr/bin/env python

import ConfigParser
from collections import defaultdict
import random
import re
import os

from flask import Flask, jsonify, make_response, request
from twython import Twython

app = Flask(__name__)


class Generate(object):
    '''
    Generates a tweet, storing words in memory, using Markov bigrams.
    '''

    def __init__(self, statuses):
        self.words = self._get_words(statuses)
        self.num_words = len(self.words)
        self.tokens = defaultdict(list) # maps (w2, w2 -> [w3, w4]) for every pair w1, w2
        self._triples()

    def _get_words(self, statuses):
        '''
        Returns words in given statuses without any @ mentions, or hashtags.
        '''
        words = []
        for status in statuses:
            for word in status.split():
                words.append(word.lower())
        return words

    def _triples(self):
        '''
        Builds the tokens dictionary. For each (w1, w2, w3), maps
        (w1, w2) -> w3.
        '''
        if self.num_words < 3: return
        for i in xrange(self.num_words - 2):
            key = (self.words[i], self.words[i + 1])
            next_word = self.words[i + 2]
            self.tokens[key].append(next_word)

    def generate(self, n=20, size=6):
        '''
        Generate a tweet of given word size.
        '''
        result = []
        for _ in range(n):
            seed_num = random.randint(0, self.num_words - 3) # this will be w1
            w1, w2 = self.words[seed_num], self.words[seed_num + 1]
            gen_words = []

            for i in xrange(size):
                gen_words.append(w1) # add w1
                if self.tokens[(w1, w2)] == []:
                    break
                w1, w2 = w2, random.choice(self.tokens[(w1, w2)]) # get a random w3 from list mapped to by (w1, w2)
            gen_words.append(w2)
            result.append(' '.join(gen_words))
        return result


@app.route('/', methods=['GET'])
def index():
    return make_response(open('templates/index.html').read())


@app.route('/get_tweets/<screen_name>', methods=['GET'])
def do(screen_name):
    app_key = os.environ.get('APP_KEY')
    app_secret = os.environ.get('APP_SECRET')
    screen_name = str(screen_name)
    twitter = Twython(app_key, app_secret)
    timeline = twitter.get_user_timeline(screen_name=screen_name,
                                         count=200, exclude_replies=True,
                                         include_rts=False)
    statuses = [status['text'] for status in timeline]

    g = Generate(statuses)

    tweets = g.generate(size=random.randint(4, 7))

    return jsonify(tweets=tweets)


if __name__ == '__main__':
    app.run(debug=True)
