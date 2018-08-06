# Twitter Export

You've decided to quit or cut down your Twitter footprint. Here's some help.

Export your data export by [exporting your tweet archive](https://twitter.com/settings/account).

You're on your way. That's where this code comes in.

## Requirements

You must have NodeJS installed. `brew install nodejs` usually does the trick on
Macs.

## Process

1. clone this repo to a local machine and `cd` into it
1. put the file `tweet.js`, from your tweet archive export into the local clone
1. run `./export_tweets.js`
1. Look in `converted_tweets`

```text
converted_tweets
├── 2008
│   ├── 08
│   │   ├── 22
│   │   │   ├── 2008-08-22-895722280.tweet.json
│   │   │   ├── 2008-08-22-895741518.tweet.json
│   │   │   ├── 2008-08-22-895834676.tweet.json
│   │   │   ├── 2008-08-22-895999543.tweet.json
│   │   │   ├── 2008-08-22-896021129.tweet.json
│   │   │   ├── 2008-08-22-896076861.tweet.json
```

```json
$ more ./converted_tweets/2008/08/22/2008-08-22-895722280.tweet.json
{"coordinates":null,"retweeted":false,"source":"<a href=\"http://twitter.com\" rel=\"nofollow\">Twitter Web Client</a>","entities":{"hashtags":[],"symbols":[],"user_mentions":[],"urls":[]},"display_text_range":["0.0","128.0"],"favorite_count":"0.0","in_reply_to_status_id_str":null,"geo":null,"id_str":"895722280","in_reply_to_user_id":null,"truncated":false,"retweet_count":"0.0","id":"8.9572228E8","in_reply_to_status_id":null,"created_at":"Fri Aug 22 17:19:38 +0000 2008","place":null,"favorited":false,"full_text":"I just joined twitter after disparaging it, hating it, not getting it and generally thinking it kinda sucked.  Hell much colder.","lang":"en","contributors":null,"in_reply_to_screen_name":null,"in_reply_to_user_id_str":null}
```

With your tweets split up like this, you can feel secure that you can go
through deleting your history at Twitter.

## Advice

Having split up my archive, I put the information in git. I'd recommend you do
the same.

## Next Steps for Deleters

I'm then going to go through the tweets and move the Tweets I like to Hugo, my
blogging platform.  All the others, I will delete and track via git. Then I'll
be able to look at the JSON for the items that were removed and use the Twitter
API to delete them.
