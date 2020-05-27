"""
this is to collect all the twitter lists owned by media accounts
http://docs.tweepy.org/en/latest/api.html#list-methods
using API.lists_all

Returns all lists the authenticating or specified user subscribes to, including their own. The user is specified using the user_id or screen_name parameters.

A maximum of 100 results will be returned by this call. Subscribed lists are returned first, followed by owned lists. This means that if a user subscribes to 90 lists and owns 20 lists, this method returns 90 subscriptions and 10 owned lists. The reverse method returns owned lists first, so with reverse=true, 20 owned lists and 80 subscriptions would be returned.

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


def owned_list_all(screen_name):
    try:
        lists = []
        for item in api.lists_all(screen_name = screen_name):
            lst_json = item._json
            lists.append(lst_json)
        return (lists)

    except tweepy.TweepError as e:
        error_code = e.response.status_code
        return (error_code)


# Main function
if __name__ == '__main__' :
     #API used: jiajun2_API
    #Api:
    #Api:
    [CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET] = twitter_API(keys.jiajun1_API)

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    #api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=2, retry_delay=15)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    media_lst = ["EconUS", "BBCWorld", "NPR", "NewsHour", "WSJ", "ABC",
        "CBSNews", "NBCNews", "CNN", "USATODAY", "theblaze",
        "nytimes", "washingtonpost", "msnbc", "GuardianUS",
         "Bloomberg", "NewYorker", "politico", "YahooNews",
         "FoxNews", "MotherJones", "Slate", "BreitbartNews",
         "HuffPostPol", "StephenAtHome", "thinkprogress",
         "TheDailyShow", "DRUDGE_REPORT", "dailykos", "seanhannity",
         "AJENews", "edshow", "glennbeck", "BuzzFeedPol"]

    count = 0

    for media_accout in media_lst:

        count += 1

        media_owned_list = owned_list_all(media_accout)

        if type(media_owned_list) == list:
            print (media_accout, len(media_owned_list))

            lst_filename = "~/media_own_lists/{}.json".format(media_accout)
            with open(lst_filename, 'w') as outfile:
                for entry in media_owned_list:
                    json.dump(entry, outfile)
                    outfile.write('\n')
        else:
            print (media_accout, media_owned_list)
