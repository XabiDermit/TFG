import configparser
import tweepy
import webbrowser

config = configparser.ConfigParser()
config.read('../info.properties')

consumer_key = config.get('APIkey', 'consumer_key')
consumer_secret = config.get('APIkey', 'consumer_secret')


def kontuarekinkautotu():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # aplikazioa autorizatzeko uri-a lortu eta nabigatzailean ireki
    auth_url = auth.get_authorization_url()
    webbrowser.open(auth_url)
    return auth


def kontugabekautotu():
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    for tweet in tweepy.Cursor(api.search, q='tweepy').items(10):
        print(tweet.text)


def autorizatu(auth, pin):
    auth.get_access_token(pin)
    print('ACCESS_KEY = "%s"' % auth.access_token)
    print('ACCESS_SECRET = "%s"' % auth.access_token_secret)

    # authenticate and retrieve user name
    auth.set_access_token(auth.access_token, auth.access_token_secret)
    api = tweepy.API(auth)
    return api

