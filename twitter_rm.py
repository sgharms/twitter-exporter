#!/usr/bin/env python3

import os
import twitter
import pdb

TWEET_DOES_NOT_EXIST_CODE=144

# Ensure these environment variables are set with twitter access codes.
api = twitter.Api(consumer_key=os.environ["CONSUMER_KEY"],
        consumer_secret=os.environ["CONSUMER_SECRET"],
        access_token_key=os.environ["ACCESS_TOKEN"],
        access_token_secret=os.environ["ACCESS_TOKEN_SECRET"])

fh = open("deletables.txt")
status_id = fh.readline().rstrip()

while status_id:
    print("Processing {}".format(status_id))

    try:
        result = api.DestroyStatus(status_id)
    except twitter.error.TwitterError as e:
        if e.message[0]['code'] == TWEET_DOES_NOT_EXIST_CODE:
            print("Skipped " + status_id)
            pass

    status_id = fh.readline().rstrip()

