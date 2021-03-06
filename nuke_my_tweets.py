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

# Nuke My Tweets configurations
tweets_history_preserve = config.get('tweets', 'history_preserve').split(',')
tweets_history = config.get('tweets', 'history_file')

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

print('OAuth successful \nloading tweets')


with open(tweets_history, 'r') as f:
    data = json.load(f)
    tweets_list = data['tweets']

print('Begin nuke: Status')
print('=====================================')
n = u'\u2713'
for tweet in tweets_list:
    tweet_id = tweet['id']

    # Don't delete preserved tweets
    if (tweet_id in tweets_history_preserve):
        print(f'preserved tweet {tweet_id}')
        continue

    # Delete the tweet
    if args.accept:
        try:
            api.destroy_status(tweet_id)
            # print("dangerously deleted tweet")
        except tweepy.error.TweepError:
            print(f'skipped operation on {tweet_id}')

    print(f'deleted tweet {tweet_id} [{n}]')

print('=====================================')
print('Mission complete!')
