import os
import sys
import twitter

api = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
                  consumer_secret=os.environ['CONSUMER_SECRET'],
                  access_token_key=os.environ['ACCESS_TOKEN'],
                  access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])

recent_tweets = api.GetUserTimeline(screen_name=sys.argv[1])
for t in recent_tweets:
    print(f"{t.id}|{t.created_at}|{t.text}")
     
