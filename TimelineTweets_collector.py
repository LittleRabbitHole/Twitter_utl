"""
this is to collect twitter user's most recent 3000 timeline tweets
input a list of user ids
output .json file (including the most recent 3000 tweets) for each user
"""

import pandas as pd
import tweepy
import json
import argparse
import keys

def twitter_API(APIkeys):
    CONSUMER_KEY = APIkeys['CONSUMER_KEY']
    CONSUMER_SECRET = APIkeys['CONSUMER_SECRET']
    ACCESS_TOKEN = APIkeys['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = APIkeys['ACCESS_TOKEN_SECRET']
    return ([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET])


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

def tweet_timeline(uid):#total=100

    try:
        user_tweets = []
        for item in limit_handled(tweepy.Cursor(api.user_timeline, user_id = uid, count=200).items()):#total
            tweet_json = item._json
            user_tweets.append(tweet_json)
        return (user_tweets)

    except tweepy.TweepError as e:
        error_code = e.response.status_code
        return (error_code)
        #error_uid[error_code] = uid


# Main function
if __name__ == '__main__' :

    # parser = argparse.ArgumentParser(description='select API')
    # parser.add_argument('-api', '--keys', help='select API keys to use')
    # parser.add_argument('-usrS', '--usrS', help='select user lsts')
    # args = parser.parse_args()
    # api_name = args.keys
    # user_lst_startPosition = int(args.usrS)

    [CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET] = twitter_API(keys.jiajun2_API)

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    #api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=2, retry_delay=15)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    retweet_user_df = pd.read_pickle("~/original_contributors.p")
    user_ids = list(retweet_user_df['orig_user_id'])

    #collect data & write out
    error_uid = {}

    c=0
    for uid in user_ids:
        c+=1

        timeline_tweet = tweet_timeline(uid)

        if type(timeline_tweet) != int:
            tweet_filename = "~/tweets_json/{}.json".format(str(uid))
            with open(tweet_filename, 'w') as outfile:
                for entry in timeline_tweet:
                    json.dump(entry, outfile)
                    outfile.write('\n')
        else:
            error_code = timeline_tweet
            try:
                error_uid[error_code].append(uid)
            except KeyError:
                error_uid[error_code] = []
                error_uid[error_code].append(uid)

        if c%100==0:
            print (c)

    error_filename = "~/error/error.json"
    with open(error_filename, 'w') as errorfile:
        json.dumps(error_uid, errorfile)
