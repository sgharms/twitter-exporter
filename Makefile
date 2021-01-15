generate_id_list:
	docker run --env-file twitter_secrets -v $$(pwd):/workarea -it --rm twimg python get_recent_tweets.py $$TWITTER_ID > deletables.txt

delete_ids_from_deletables:
	docker run --env-file twitter_secrets -v $$(pwd):/workarea -it --rm twimg python twitter_rm.py

.PHONY: delete_ids_from_deletables generate_id_list
