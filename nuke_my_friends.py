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

print('OAuth successful \nloading tweets')

# Nuke My Tweets configurations
followers = config.get('friendship', 'followers_file')
following = config.get('friendship', 'following_file')

with open(followers, 'r') as f:
    data = json.load(f)
    followers_list = data['followers']

with open(following, 'r') as f:
    data = json.load(f)
    following_list = data['following']

print('Begin nuke: Friends')
print('=====================================')
n = u'\u2713'

following_all = []
followers_all = []
remove_all = []
add_all = []
added = 0
removed = 0

for friend in following_list:
    following_all.append(friend['following']['accountId'])

for fan in followers_list:
    followers_all.append(fan['follower']['accountId'])

print(followers_all)
print(following_all)

for person in following_all:
    if(person not in followers_all):
        remove_all.append(person)

for new_person in followers_all:
    if(person not in following_all):
        add_all.append(new_person)

for person_to_remove in remove_all:
    try:
        if args.accept:
            api.destroy_friendship(person_to_remove)
        print(f'unfollowed {person_to_remove}')
        removed += 1
    except tweepy.error.TweepError:
        print(f'skipped operation on {person_to_remove}')

for person_to_add in remove_all:
    try:
        if args.accept:
            api.create_friendship(person_to_add)
        print(f'followed {person_to_add}')
        added += 1
    except tweepy.error.TweepError:
        print(f'skipped operation on {person_to_add}')

print(f'You removed {removed} people and added {added} people on twitter')

print('=====================================')
print('Mission complete!')
