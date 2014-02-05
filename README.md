What would I tweet
==================

**What would I tweet** automatically generates tweets for you! It trains a Markov bot based on bigram probabilities derived from your tweet history.

The app is built using:

- Python (Flask) in the backend. It provides a RESTful interface for generating tweets for a username. See the [end-point](https://github.com/karan/What-Would-I-Tweet/blob/master/gen.py#L69).
- AngularJS provides the client side manipulations and real-time interaction.

Usage
======

Get your `app_key` and `app_secret` from [Twitter Dev Center](https://dev.twitter.com/apps/new).

Create `settings.cfg` with the following content:

    [auth]
    app_key=xxxxxxxxxxxxxx
    app_secret=xxxxxxxxxxxxxxxxxxxxxxxxxx

Run the script:

    $ python gen.py

Open `localhost:5000` in your browser.