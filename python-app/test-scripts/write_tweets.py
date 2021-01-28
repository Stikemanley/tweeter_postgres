import tweepy
import os
from psycopg2 import connect

auth = tweepy.OAuthHandler(os.getenv('consumer_key'), os.getenv('consumer_secret'))
auth.set_access_token(os.getenv('access_token'), os.getenv('access_token_secret'))

api = tweepy.API(auth)

def get_user_tweets(userId, tweet_count=10):
    tweets = api.user_timeline(screen_name=userId,
                               count=tweet_count,
                               include_rts=False,
                               tweet_mode='extended')
    # for info in tweets[:3]:
    #
    #     print('ID: {}'.format(info.id))
    #     print(info.created_at)
    #     print(info.full_text)

    return tweets

def write_tweets_to_table(tweets,userId):
    conn = connect(
        dbname="twitter",
        user="michael.stanley",
        host="172.28.1.4",
        password="password"
    )

    cur = conn.cursor()

    command = '''INSERT INTO tweets (tweet_id, tweet_text, user_id, created_Date) VALUES (%s,%s,%s,%s)'''
    for tweet in tweets:
        # print(command.format(tweet.id,tweet.full_text,userId,tweet.created_at))
        print(tweet.full_text)
        print(tweet.id)
        cur.execute(command,(tweet.id,tweet.full_text,userId,tweet.created_at))
    conn.commit()
    cur.close()
    conn.close()

tweets = get_user_tweets('SpeakerPelosi')
write_tweets_to_table(tweets,'SpeakerPelosi')

# def db_initpop(bundle):
#     """
#     This function places basic tweet features in the database.  Note the placeholder values:
#     these can act as a check to verify that no further expansion was available for that method.
#     """
#     #unpack the bundle
#     tweet_id, user_sn, retweet_count, tweet_text = bundle
#     curs.execute("""INSERT INTO twitter VALUES (null,?,?,?,?,?,?)""", \
#         (tweet_id, user_sn, retweet_count, tweet_text, 'cleaned text', 'cleaned retweet text'))
#     conn.commit()
#     print 'Database populated with tweet '+str(tweet_id)+' at '+time.strftime("%d %b %Y %H:%M:%S", time.localtime())