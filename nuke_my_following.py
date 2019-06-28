#!/bin/python3
"""
Python script to delete all tweets from a twitter account

This script uses twitter history data. Download it from twitter
account settings.

Configure the keys, path to tweets.csv, and tweets to preserve
in scripts.ini file
"""
import configparser
import argparse
import tweepy
import json

# Load script configurations
config = configparser.ConfigParser()
config.read('scripts.ini')

# Twitter app configurations
consumer_key = config.get('consumer', 'api_key')
consumer_secret = config.get('consumer', 'api_secret')
access_token = config.get('access', 'token')
access_token_secret = config.get('access', 'token_secret')

# Get runtime parameters
parser = argparse.ArgumentParser(description='Nuke My Tweets v1.0.9')
parser.add_argument('-a', '--accept', help='Live run', action='store_true')
args = parser.parse_args()

# Dry run notification
if args.accept:
    print('Mission start \nLive run')
    print('=====================================')
else:
    print('Mission start \nDry run')
    print('=====================================')

# Log into Twitter
print('OAuth sent')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

print('OAuth successful \nloading following')

# Nuke My Tweets configurations
following = config.get('friendship', 'following_file')

with open(following, 'r') as f:
    data = json.load(f)
    following_list = data['following']

print('Begin nuke: Following')
print('=====================================')

n = u'\u2713'
removed = 0

for item in following_list:
    person = item['following']['accountId']

    try:
        if args.accept:
            api.destroy_friendship(person)
        print(f'unfollowed {person}')
        removed += 1
    except tweepy.error.TweepError:
        print(f'skipped operation on {person}')

print(f'You removed {removed} people people on twitter')

print('=====================================')
print('Mission complete!')
