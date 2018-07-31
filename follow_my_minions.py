#!/bin/python3
"""
Python script to follow all twitter accounts in minions.csv
Minions.csv has twitter accounts listed on http://www.letsallfollowback.com/
TODO: Scrape https://followback.com/
"""
import configparser
import argparse
import tweepy
import csv

# Load script configurations
config = configparser.ConfigParser()
config.read('scripts.ini')

# Twitter app configurations
consumer_key = config.get('consumer', 'api_key')
consumer_secret = config.get('consumer', 'api_secret')
access_token = config.get('access', 'token')
access_token_secret = config.get('access', 'token_secret')

# Follow My Minions configurations
# TODO: Create a blacklist
twitter_minion_blacklist = config.get('minions', 'followers_csv').split(',')
twitter_minions_csv = config.get('minions', 'followers_csv')
twitter_minions_per_day = int(config.get('minions', 'followers_per_day'))

# Get runtime parameters
parser = argparse.ArgumentParser(description='Follow My Minions v1.0.0')
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
with open(twitter_minions_csv, 'r') as f:
    reader = csv.reader(f)

    # Skip header
    next(reader, None)

    # Convert CSV to list
    minions_list = list(reader)

print('Begin nuke')
print('=====================================')

# TODO: Read from file and assign to friendships_count
friendships_count = 0
check = u'\u2713'

# TODO: Skip CSV records to match friendships_count as start
for minion in minions_list:
    # Limit break
    if friendships_count >= twitter_minions_per_day:
        print('Reached limit at %d' % (friendships_count))
        # TODO: Write to file and exit
        break

    # tweet[0] is the tweet_id column
    minion_id = minion[0]

    # Don't delete preserved tweets
    if (minion_id in twitter_minion_blacklist):
        print('[ ] follow @%s' % (minion_id))
        continue

    # Delete the tweet
    if args.accept:
        # api.create_friendship(minion_id)
        friendships_count += 1
        print("dangerously follow minions")

    print('[%s] follow @%s' % (check, minion_id))

print('=====================================')
print('Mission complete!')
