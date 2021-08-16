import tweepy
import socket
import re

# Enter your Twitter keys here!!!
ACCESS_TOKEN = ""
ACCESS_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

# API authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# create wrapper
api = tweepy.API(auth)

#hashtag used to pull data
hashtag = "#palestine"

#file name to store data for viewing
filename = "TweetScrapper.csv"

# stream location
TCP_IP = 'localhost'
TCP_PORT = 9001


def preprocessing(tweet):
    # Add here your code to preprocess the tweets and
    # remove Emoji patterns, emoticons, symbols & pictographs, transport & map symbols, flags (iOS), etc
    # remove additional spacing as well
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff]+", flags=re.UNICODE)
    tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)
    text = emoji_pattern.sub(r'', tweet)
    text = text.replace("\n", " ")
    return text


def getTweet(status):
    # You can explore fields/data other than location and the tweet itself.
    # Check what else you could explore in terms of data inside Status object

    tweet = ""
    location = ""

    location = status.user.location

    if hasattr(status, "retweeted_status"):  # Check if Retweet
        try:
            tweet = status.retweeted_status.extended_tweet["full_text"]
        except AttributeError:
            tweet = status.retweeted_status.text
    else:
        try:
            tweet = status.extended_tweet["full_text"]
        except AttributeError:
            tweet = status.text

    return location, preprocessing(tweet)


# create sockets
# comment out if current distro is not set up to be streamed
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()


# error handling
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        location, tweet = getTweet(status)

        if (location != None and tweet != None):
            tweetLocation = location + "::" + tweet + "\n"
            print(location, status.text)
            # comment out if current distro is not set up to be streamed
            conn.send(tweetLocation.encode('utf-8'))

        return True

    def on_error(self, status_code):
        if status_code == 420:
            return False
        else:
            print(status_code)


# stream listener creation
myStream = tweepy.Stream(auth=auth, listener=MyStreamListener())
myStream.filter(track=[hashtag], languages=["en"])
