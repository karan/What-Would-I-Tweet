#!/usr/bin/env python

import ConfigParser


config = ConfigParser.ConfigParser()
config.read('settings.cfg')
app_key = config.get('auth', 'app_key')
app_secret = config.get('auth', 'app_secret')

print app_key, app_secret