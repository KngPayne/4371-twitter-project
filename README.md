# Objective
The project is to scrape tweets for sentiment analysis of particular hashtags from twitter in real time. 
There are two scripts to scrape tweets for data analysis. Tweets are retrieved using tweepy a python twitter API and analyzed using textBlob for sentiment.

# Purpose
Grabbing real time data around a topic on twitter and visualizing data on a dashboard in Kibana.

# 1. Installation and usage
The program is meant to be run in a unix environment. As twitter is the stream source a twitter dev account will be needed. 

***Source info***
1. Create an account at https://apps.twitter.com/
2. Click on **Create an App** to create your own twitter app
3. Fill out the form and submit
4. Once the app is made there will be a form with app details. Click on **Keys and Tokens** and generate keys
5. Four keys will be needed
   - Consumer key (API key)
   - Consumer secret (API secret key)
   - Access token 
   - Access token secret

Below is a list of required software meant to be installed. 

***Required software:*** 
- ElasticSearch
- Kibana
- Apache spark
- Hadoop

## **1.2 Putting it together**
Before running the files ensure that all keys have been put into their respective files. 
**Stream.py** will require all twitter keys that were generated when creating a twitter app
**Spark.py** will require the cloud id for elasticsearch  and the http auth.

After all necessary keys have been entered and saved into their files. Put in the requested search word in **stream.py** then save the file. 
The sentiment analysis can be adjusted or swapped for a different version in **Spark.py** if requested

**Running the program:**
1. Ensure all software required is installed
2. Run Stream.py
3. Run Spark.py
4. Have Kibana receiving data 

# 2. Output
All data should be gathered and recieved by elasticSearch. Using kibana you can configure the dashboard as you please to display the data you have
If needed it can also be set up to recieve using a geo heatmap though this would require work on kibanas end based on how you wish to display

When looking at the data being streamed do keep in mind that due to privacy and ethics reasons locations will be grabbed from users profiles based on what they have entered.
