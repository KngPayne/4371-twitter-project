from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from textblob import TextBlob
from elasticsearch import Elasticsearch
from ftfy import fix_text
from googletrans import Translator
from geopy.geocoders import Nominatim

TCP_IP = 'localhost'
TCP_PORT = 9001


# initialzie geolocator and start translator
# translator = Translator()
#
#
# clean tweet locations into english
# def clean_text(text, engl=True):
#     if engl:
#         trans_word = text
#     else:
#         trans_word = translator.translate(text).text
#
#     token_text = []
#     text = trans_word
#     text = [fix_text(str(i)) for i in text]
#
#    return text

def processTweet(tweet):
    # Here, are the implementations:
    # (i) Sentiment analysis,
    # (ii) Get data corresponding to place where the tweet was generate (using geopy or googlemaps)
    # (iii) Index the data using Elastic Search

    # Elastic search initialization
    cloud_id = 'insert kibana key here'
    es = Elasticsearch(cloud_id=cloud_id, http_auth=('elastic', 'elastic search id'))

    tweetData = tweet.split("::")

    if len(tweetData) > 1:

        text = tweetData[1]
        rawLocation = tweetData[0]

        # (i) Apply Sentiment analysis in "text"
        if float(TextBlob(text).sentiment.polarity) > 0.3:
            sentiment = "Positive"
        elif float(TextBlob(text).sentiment.polarity) < -0.3:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        # (ii) Get geolocation (state, country, lat, lon, etc...) from rawLocation
        try:
            geolocator = Nominatim(user_agent="bts")
            location = geolocator.geocode(tweetData[0], exactly_one=True, addressdetails=True)
            lat = location.raw['lat']
            lon = location.raw['lon']
            state = location.raw['address']['state']
            country = location.raw['address']['country']
        except:
            lat = lon = state = country = None

        print("\n\n=========================\ntweet: ", tweet)
        print("Raw location from tweet status: ", rawLocation)
        # print("lat: ", lat)
        # print("lon: ", lon)
        # print("state: ", state)
        # print("country: ", country)
        # print("Text: ", text)
        # print("Sentiment: ", sentiment)

        # (iii) Post the index on ElasticSearch or log your data in some other way (you are always free!!)
        if lat != None and lon != None and sentiment != None:
            esDoc = {"location": {"lat": lat, "lon": lon}, "state": state, "country": country, "sentiment": sentiment}
            es.index(index='tweet-geo', doc_type='default', body=esDoc)


# Pyspark
# create spark configuration
conf = SparkConf()
conf.setAppName('TwitterApp')
conf.setMaster('local[2]')

# create spark context with the above configuration
sc = SparkContext(conf=conf)

# create the Streaming Context from spark context with interval size 4 seconds
ssc = StreamingContext(sc, 4)
ssc.checkpoint("checkpoint_TwitterApp")

# read data from port 900
dataStream = ssc.socketTextStream(TCP_IP, TCP_PORT)

# process eachRDD apply processTweet
dataStream.foreachRDD(lambda rdd: rdd.foreach(processTweet))

ssc.start()
ssc.awaitTermination()
