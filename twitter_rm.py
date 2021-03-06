#!/usr/bin/env python3

import os
import twitter
import sys
import pdb

TWEET_DOES_NOT_EXIST_CODE=144

# Ensure these environment variables are set with twitter access codes.
api = twitter.Api(consumer_key=os.environ["CONSUMER_KEY"],
        consumer_secret=os.environ["CONSUMER_SECRET"],
        access_token_key=os.environ["ACCESS_TOKEN"],
        access_token_secret=os.environ["ACCESS_TOKEN_SECRET"])

def extract_status_id(inp):
    return inp.split('|')[0]

fn = lambda: sys.argv[1] if sys.argv[1:] else "deletables.txt"
fh = open(str(fn()))

next_line = fh.readline().rstrip()

while next_line:
    status_id = extract_status_id(next_line)

    try:
        status_id_to_i = int(status_id)
        status_id = status_id_to_i
    except ValueError:
        next_line = fh.readline().rstrip()
        continue

    print(f"Processing {status_id}")

    try:
        result = api.DestroyStatus(status_id)
    except twitter.error.TwitterError as e:
        if e.message[0]['code'] == TWEET_DOES_NOT_EXIST_CODE:
            print(f"Skipped {status_id}")
            pass

    next_line = fh.readline().rstrip()
    
