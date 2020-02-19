import pandas as pd
import tweepy
import json
import re
import pickle
import argparse
import time

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


def tweet_followers(uid):#total=100
    backoff_counter = 1
    while True:
        try:
            user_followers = []
            for item in limit_handled(tweepy.Cursor(api.followers_ids, user_id =uid, count = 5000, cursor=-1, stringify_ids=True).items()):
                user_followers.append(item)
            return (user_followers)
            break
        except tweepy.TweepError as e:
            try:
                error_code = e.response.status_code
                return (error_code)
                break
            except:
                print(e.reason)
                print (uid)
                time.sleep(backoff_counter * 60)
                backoff_counter += 1
                continue

                
                
def tweet_friends(uid):
    backoff_counter = 1
    while True:
        try:
            user_followers = []
            for item in limit_handled(tweepy.Cursor(api.friends_ids, user_id =uid, count = 5000, cursor=-1, stringify_ids=True).items()):
                user_followers.append(item)
            return (user_followers)
            break
        except tweepy.TweepError as e:
            try:
                error_code = e.response.status_code
                return (error_code)
                break
            except:
                print(e.reason)
                print (uid)
                time.sleep(backoff_counter * 60)
                backoff_counter += 1
                continue
                

# Main function
if __name__ == '__main__' :
    
    API = {
        'CONSUMER_KEY':'xxx',
        'CONSUMER_SECRET':'xxx',
        'ACCESS_TOKEN':'xxx',
        'ACCESS_TOKEN_SECRET': 'xxx'
    }

    
    
    [CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET] = twitter_API(API)
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    #api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=2, retry_delay=15)    
    
    #read your twitter account list of userids
    mediaAccounts_lst = pd.read_pickle("account_user_ids.p")
    
    #write out
    outfile = open("~/connections.csv", "w")
    
    
    count = 0 
    for uid in mediaAccounts_lst:
        count+=1 
                
        #followers
        follower_list = tweet_followers(uid)
        
        #friends
        #friends_list = tweet_friends(uid)
        
        if type(follower_list) == list:
            print (count, uid, len(follower_list))
            
            result_lst_str = [uid] + follower_list
            line_string = ",".join(result_lst_str)+"\n"
            outfile.write(line_string)
            
        else:
            print ("error", count, uid, follower_list)
            
    outfile.close() 
    
    
    
    
    
    
    
    
    