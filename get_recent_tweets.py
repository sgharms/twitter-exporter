import os
import re
import sys
import twitter

api = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
                  consumer_secret=os.environ['CONSUMER_SECRET'],
                  access_token_key=os.environ['ACCESS_TOKEN'],
                  access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])

recent_tweets = api.GetUserTimeline(screen_name=sys.argv[1], count=200, include_rts=True)
for t in recent_tweets:
    text_sans_newlines = re.sub(r'\n', '', t.text)
    print(f"{t.id}|{t.created_at}|{text_sans_newlines}")
     
