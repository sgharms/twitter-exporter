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

fh = open(str(sys.argv[1]) or "deletables.txt")
next_line = fh.readline().rstrip()

while next_line:
    status_id = extract_status_id(next_line)

    print(f"Processing {status_id}")

    try:
        result = api.DestroyStatus(status_id)
    except twitter.error.TwitterError as e:
        if e.message[0]['code'] == TWEET_DOES_NOT_EXIST_CODE:
            print(f"Skipped {status_id}")
            pass

    next_line = fh.readline().rstrip()
    
