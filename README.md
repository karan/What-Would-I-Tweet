What-Would-I-Tweet
==================

A tweet generator (playing with twitter's API)

Usage
======

Get your `app_key` and `app_secret` from [Twitter Dev Center](https://dev.twitter.com/apps/new).

Create `settings.cfg` with the following content:

    [auth]
    app_key=xxxxxxxxxxxxxx
    app_secret=xxxxxxxxxxxxxxxxxxxxxxxxxx

Run the script:

    $ python gen.py


# Notebook:

Library: https://github.com/ryanmcgrath/twython
Based on: http://what-would-i-say.com/

Will use either Markov, or occurence of each word at each position.