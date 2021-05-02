import configparser
import tweepy


### OAUTH 2 ###


### OAUTH 1 ###

config = configparser.ConfigParser()
config.read('../info.properties')

consumer_key = config.get('APIkey', 'consumer_key')
consumer_secret = config.get('APIkey', 'consumer_secret')


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')