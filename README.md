# Twitter Exporter

## Primary Use Cases

1. You want to export your Twitter data into small files that can be further
   processed (perhaps into posts for a statically-generated site?)
2. You periodically want to enforce a time-to-live on your tweets shorter
   than...forever

## Step 0: Understand the Plan

The basic operation is to:

1. Get tweets with their unique ID
2. Create a list of unique IDs to delete
3. Provide a list of "deletables" to to `twitter_rm.py`

## Step 1: Export Your Archive

[Export your tweet archive](https://twitter.com/settings/account). It's
probably worth putting this raw export into version control.

## Step 2: Factor Tweets into Files

Put the file `tweet.js`, from your tweet archive export, into your local clone
of this repository.  Use `export_tweets.js` to pull all your tweets into files
Look in the `converted_tweets`

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

Here's what's inside one of those files:

```json
$ more ./converted_tweets/2008/08/22/2008-08-22-895722280.tweet.json
{"coordinates":null,"retweeted":false,"source":"<a href=\"http://twitter.com\" rel=\"nofollow\">Twitter Web Client</a>","entities":{"hashtags":[],"symbols":[],"user_mentions":[],"urls":[]},"display_text_range":["0.0","128.0"],"favorite_count":"0.0","in_reply_to_status_id_str":null,"geo":null,"id_str":"895722280","in_reply_to_user_id":null,"truncated":false,"retweet_count":"0.0","id":"8.9572228E8","in_reply_to_status_id":null,"created_at":"Fri Aug 22 17:19:38 +0000 2008","place":null,"favorited":false,"full_text":"I just joined twitter after disparaging it, hating it, not getting it and generally thinking it kinda sucked.  Hell much colder.","lang":"en","contributors":null,"in_reply_to_screen_name":null,"in_reply_to_user_id_str":null}
```

## Step 3: Build a List of Deletables

There are a lot of ways to go about building this list. Given a collection of
tweets as independent files (i.e. after using `export_tweets.js`), `query.py`
can provides a menu-based interface to decide which IDs are added to
`deletables.txt`. This file can then be processed. A lower-fi version will be
discussed subsequently.


`./query.py (subdir)`

```shell
$ ./query.py 2008`
```

![Preview of Interface with my first Tweet](./ui_preview.png)

_My First Tweet: time to go!_

Hat Tip: [Clayton McCloud's ncurses demo](https://gist.github.com/claymcleod/b670285f334acd56ad1c)

Here I'm going to find all the exported tweets in `2008`. I _could_ do
`2008/08`.  The goal is to make deleting easy. We use a dating-app-like
interface to arrange Death + Our tweet.

* **RIGHT**: Adds the tweet id to `deletables.txt` which we can feed to the
  twitter API to do the finale remove later. **THIS ALSO DELETES THE FILE FROM
  LOCAL STORAGE**
* **LEFT**: Adds the tweet id to `deletables.txt` which we can feed to the
  twitter API to do the finale remove later. This **DOES NOT** remove the local
  file. You might reuse this content for a book, or a scrapbook, or import into
  come other CMS.

**CAVEAT**: This menu is not very smart and may not work (right, at all) in
narrow widths. Should be fine at 80 x 40. This is write-once code. Bugs and
snarly code to be expected.

Perhaps you can't use an `ncurses` menu-driven program like `query.py`.  If all
the files are under `git` revision control, an alternative approach might be
something as simple as:

```bash
for file in $(ls *.json); do
  jq '' $file
  rm -i $file
done
```

One could then use `git diff` and `grep` to capture the deleted IDs.

## Step 4: Delete

Delete the tweets (`twitter_rm.py`).

In order to do so, you'll need to acquire **4** developer tokens from Twitter
as documented at
[python-twitter](https://python-twitter.readthedocs.io/en/latest/getting_started.html).

I stored mine in a file called `secrets`, but the variables you should export
into the shell or the Docker environment that will run your tasks are:

```text
CONSUMER_KEY
CONSUMER_SECRET
ACCESS_TOKEN
ACCESS_TOKEN_SECRET
```

An invocation using a locally-installed Python might look like:

```shell
$ source secrets && PYTHONUNBUFFERED=1 ./twitter_rm.py |tee deletions.log
```

## Requirements

* `export_tweets.js` requires a Node runtime. The Docker image is fine.
* `twitter_rm.py` requires a Python runtime. The Docker image is fine as well.

## Ongoing Maintenance

If you occasionally find yourself tweeting and want to delete your payload,
follow these steps that leverage Docker.

First build the Docker image:

    docker build  .  -t twimg

Then, provided a file with the API keys called `twitter_secrets` that holds API
key data per above:

    docker run --env-file twitter_secrets -v $(pwd):/workarea -it --rm twimg python get_recent_tweets.py $TWITTER_ID |tee del

will run in the Dockerized environment:

    python get_recent_tweets.py $TWITTER_ID |tee del

and produce a list of tweets with their ID to STDOUT (and redirect into a file
called `del` per the `tee` program's specification)

We can then feed that file into:

     docker run --env-file twitter_secrets -v $(pwd):/workarea -it --rm twimg python twitter_rm.py del

And, viol&agrave; you'll remove those tweets!

