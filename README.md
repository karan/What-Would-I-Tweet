What would I tweet
==================

**What would I tweet** automatically generates tweets for you! It trains a Markov bot based on bigram probabilities derived from your tweet history.

The app is built using:

- Python (Flask) in the backend. It provides a RESTful interface for generating tweets for a username. See the [end-point](https://github.com/karan/What-Would-I-Tweet/blob/master/gen.py#L69).
- AngularJS provides the client side manipulations and real-time interaction.

Usage
======

Get your `app_key` and `app_secret` from [Twitter Dev Center](https://dev.twitter.com/apps/new).

Create environment variables.

    $ export APP_KEY=xxxxxxxxxxxxxx
    $ export APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxx

Run the script:

    $ python gen.py

Or if you have heroku toolkit:
    
    $ foreman start

Open `localhost:5000` in your browser.
