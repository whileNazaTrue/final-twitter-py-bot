import os
from credentials import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, ACCOUNT_ID, ACCOUNT_NAME

import glob
import tweepy

from tweepy import Stream
from tweepy.streaming import StreamListener
import random



class StdOutListener(StreamListener):
    def on_status(self,status):
        tweetId = status.id;
        tweet = "Bot testing.";
        print("Found a tweet. Tweet number " + status.id_str + " from user id " + str(status.user.id) + " whose username is " + status.user.screen_name)
        
        

        if status.user.screen_name == ACCOUNT_NAME:
            print("That's my own tweet! I'll ignore it.");
        elif hasattr(status,"retweeted_status")==True:
            print("That's a retweet. Not my business.");
        else:
            print("Not my tweet. Replying!")
            mediaReply(tweet,tweetId);
        #replyTweet(tweet,tweetId);
        

def authenticate():
    auth = tweepy.OAuthHandler(API_KEY,API_SECRET);
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET);
    api = tweepy.API(auth);
    return api, auth;

def streaming():
    api,auth = authenticate();
    listener = StdOutListener();
    stream = Stream(auth,listener);
    stream.filter(track=[ACCOUNT_NAME]);


def replyTweet(tweet,tweetId):
    api, auth = authenticate();
    
    api.update_status(
        tweet, 
        in_reply_to_status_id = tweetId,
        auto_populate_reply_metadata = True
    )

def pickImg():
    randNumber = random.randint(1,34);
    return str(randNumber) + ".jpg";


def mediaReply(tweet,tweetId):
    
    api, auth = authenticate();
    
    current = os.getcwd();
    os.chdir("./images/");
    media = api.media_upload(pickImg());
    

    
    api.update_status(
        tweet,
        in_reply_to_status_id = tweetId,
        auto_populate_reply_metadata = True,
        exclude_reply_user_ids = 1390871003333541892,
        media_ids = [media.media_id_string]
    )
    os.chdir(current);



if __name__ == "__main__":
    streaming();