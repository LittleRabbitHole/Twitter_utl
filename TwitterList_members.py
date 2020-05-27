"""
collect all members for a Twitter list
"""

import pandas as pd
import tweepy
import json
import re
import pickle
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


def lst_members(lst_id):
    try:
        lists = []
        for item in limit_handled(tweepy.Cursor(api.list_members, list_id =lst_id, count = 500, cursor=-1, skip_status=True).items()):
            user_json = item._json
            lists.append(user_json)
        return (lists)

    except tweepy.TweepError as e:
        error_code = e.response.status_code
        return (error_code)


# Main function
if __name__ == '__main__' :


    #API used: jiajun2_API
    #Api:
    #Api:
    [CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET] = twitter_API(keys.Keyang_API)

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    #api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=2, retry_delay=15)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    all_lsts = pickle.load(open( "~/twitter_lists.p", "rb" ))

    count = 0

    for lst_id in all_lsts:
        count += 1

        mediaAcc_list = lst_members(lst_id)

        if type(mediaAcc_list) == list:
            print (count, len(mediaAcc_list))

            lst_filename = "~/list_members_media_accounts/{}.json".format(lst_id)
            with open(lst_filename, 'w') as outfile:
                for entry in mediaAcc_list:
                    json.dump(entry, outfile)
                    outfile.write('\n')
        else:
            print (count, mediaAcc_list)
