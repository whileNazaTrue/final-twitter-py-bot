import os
from dotenv import load_dotenv
#from credentials import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, ACCOUNT_ID, ACCOUNT_NAME This is if you want to run it locally.
#If no, use dotenv

load_dotenv();

#Enviroment Variables

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

ACCOUNT_ID = os.getenv("ACCOUNT_ID")
ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")

#You must use your own api keys/tokens which you will get in developer.twitter.com
#
import glob
import tweepy

from tweepy import Stream
from tweepy.streaming import StreamListener
import random



class StdOutListener(StreamListener):
    def on_status(self,status):
        tweetId = status.id;
        phrases = ["Add a phrase here.", "Add as many as you want", "It can be only one if you wish"];
        
        tweet = random.choice(phrases);
        print("Found a tweet. Tweet number " + status.id_str + " from user id " + str(status.user.id) + " whose username is " + status.user.screen_name)
        
        try:
            if status.user.screen_name == ACCOUNT_NAME:
                print("That's my own tweet! I'll ignore it.");
            elif hasattr(status,"retweeted_status")==True:
                print("That's a retweet. Not my business.");
            else:
                print("Not my tweet. Replying!")
                mediaReply(tweet,tweetId);
        except tweepy.TweepError:
            print("There was an error while tweeting")
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
    randNumber = random.randint(1,40); ##First must be one, second number the ammmount of images
    return str(randNumber) + ".jpg"; #Image names must be named numerically.


def mediaReply(tweet,tweetId):
    
    api, auth = authenticate();
    
    current = os.getcwd();
    os.chdir("./images/"); #We move to images folder
    media = api.media_upload(pickImg());
    

    
    api.update_status(
        tweet,
        in_reply_to_status_id = tweetId,
        auto_populate_reply_metadata = True,
        exclude_reply_user_ids = 1390871003333541892,
        media_ids = [media.media_id_string]
    )
    os.chdir(current); #We return to our main folder



if __name__ == "__main__":
    streaming();
