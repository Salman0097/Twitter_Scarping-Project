# Script Author: MOHAMED SALMAN FARES

# Pip install the command below to install the dev version of snscrape library and import it
# pip install git+https://github.com/JustAnotherArchivist/snscrape.git

# Run the below command to install Pandas library and import it
# pip install pandas

# Run the below command to install pymongo library to connect to the NoSql DB and import it
# pip install pymongo

# Run the below command to install Streamlit Library to create a GUI application and import it
# pip install streamlit

# Run the below command to install datetime library to use dates and import it
# pip install datetime

import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import streamlit as st
from datetime import date

# Setting the page configuration of the streamlit application
st.set_page_config(page_title='Twitter Scrapping', page_icon=':hash:', layout='wide')
st.write('''
# Twitter Scarping :hash:
This app displays scrapped data from twitter!!''')

today = date.today()
# Declaring a user input variable for the hashtag/search
search_term = st.text_input('What do you want to search for?',)

# Declaring a user input variable for the start date and end date from which the tweets need to be fetched
from_date = st.text_input('Enter starting date as YYYY-MM-DD format', '2022-06-01')
until_date = st.text_input('Enter end date as YYYY-MM-DD format',today)

# Setting a user input to select the number of tweets to be fetched in the form of slider
maxTweets = st.slider('Select the number of tweets to be displayed : ',100, 1000)

# Creating a list to append the tweets
tweets = []

tweets_df = {}

def getTweets():
	# Using TwitterSearchScraper function of snscrape to scrape data and append tweets to list
	for i, tweet in enumerate(
			sntwitter.TwitterSearchScraper(f'{search_term} since:{from_date} until:{until_date}').get_items()):
		if i > maxTweets:
			break
		tweets.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount,
					   tweet.retweetCount, tweet.lang, tweet.source, tweet.likeCount])

	# Creating a dataframe from the tweets list above
	tweets_df = pd.DataFrame(tweets, columns=['Datetime', 'Tweet Id', 'URL', 'Content', 'Username', 'ReplyCount',
											  'RetweetCount', 'Language', 'Source', 'LikesCount'])

	# Displays the dataframes in the page
	st.dataframe(tweets_df)

	# Creating a download button to download the dataframes in the form of csv file
	st.download_button('Download CSV',
					   tweets_df.to_csv(),
					   file_name='Twitter_Data.csv',  # File name is set as Twitter_Data by default
					   mime='text/csv'
					   )
	if st.button("Upload to DB"):

		client = pymongo.MongoClient(**st.secrets["mongodb://localhost:27017/"])

		tweets_df.to_csv('C:\\Users\\ibrah\\OneDrive\\Desktop\\Twitter_Data.csv', sep=',', index=False)

		# Creating a method to read the CSV file using pandas
		df = pd.read_csv('C:\\Users\\ibrah\\OneDrive\\Desktop\\Twitter_Data.csv')

		# Storing the CSV values in the form of dictionary as MongoDB stores the values in the form of key:value pairs
		data = df.to_dict(orient='records')

		# Creating a new DataBase "Twitter_Data"
		mydb = client["Twitter_Data"]

		# Creating a collection and inserting the values
		mydb.ScarppedTweets.insert_many(data)

# Creating the button to show the tweets respective to the search term
if st.button("Show Tweets"):
	if search_term:
		getTweets()













