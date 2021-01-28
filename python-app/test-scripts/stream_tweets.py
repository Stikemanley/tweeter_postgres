import tweepy
import os
from psycopg2 import connect
import json
auth = tweepy.OAuthHandler(os.getenv('consumer_key'), os.getenv('consumer_secret'))
auth.set_access_token(os.getenv('access_token'), os.getenv('access_token_secret'))

api = tweepy.API(auth)


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        all_data = json.loads(data)

        print(all_data['id'])
        print(all_data['user'])
        print(all_data['user']['id'])
        print(all_data['user']['name'])
        print(all_data['text'])
        print(all_data['created_at'])


streamListener = StreamListener()
stream = tweepy.Stream(auth = api.auth, listener = streamListener)

stream.filter(track=['covid','pennsylvania'])