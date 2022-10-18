#Date: 18-Oct-2022
#Purpose: To read a Web page that publishes the 40 best Crypto Accounts Twitter handles, Get them, Read their Twitter Statistics like 
#Followers Count, How many they Follow, How many Tweets have they created, their Location and whether they are Verified or not
#Learning purpose to learn Twitter API, Pandas Dataframe and BeautifulSoup usage

#Import the required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import tweepy as tw

#Get the page
#page = requests.get("https://coinme.com/10-crypto-twitter-accounts-everyone-should-follow/")
#The Page we are trying to look for is the Top Twitter Accoounts that are Good for Crypto related details
page = requests.get("https://consensys.net/blog/news/i-read-crypto-twitter-for-hours-daily-here-are-the-40-accounts-that-really-matter/")

#Use BeautifulSoup to Parse the Page
soup = BeautifulSoup(page.content, 'html.parser')

# open the file in w mode
# set encoding to UTF-8
#with open("/Users/deshmukhr/Deshmukh/Learning/python/output.html", "w", encoding = 'utf-8') as file:
    
    # prettify the soup object and convert it into a string
    #file.write(str(soup.prettify()))

#Find all the href URLs which point to twitter.com address
twitter_urls = soup.find_all(href=re.compile("^https://twitter.com/"))#soup.find_all('a', href=True)

handle_list = []
#Loop through the Twitter URLs received from the page
for temp_url in twitter_urls:
    #print(inf.get('href'))
    #Get the URL pointed by the href
    temp = temp_url.get('href')
    #In our case the Twitter URL is the 3rd on the index of the information retrieved
    twitter_handle = temp.split('/')[3]
    #Eliminate any references to the Query Strings
    twitter_handle = twitter_handle[:twitter_handle.find('?')]
    #print(twitter_handle)
    #Add the Twitter Handle to a List
    handle_list.append(twitter_handle)

#Create a DataFrame from the Twitter Handles List
handle_df = pd.DataFrame(handle_list, columns=['Handles'])
#print (handle_df.count())

#Find Duplicates and Eliminate them from the DataFrame
handle_df = handle_df.drop_duplicates()

#Now process the Twitter Handles and Get the Relevant Tweet Information of these Influencers
tw_api_key = "API Key"
tw_api_secret = "API Secret"
tw_access_token = "Access Token"
tw_access_token_secret = "Access Token Secret"

auth = tw.OAuthHandler(tw_api_key, tw_api_secret)
auth.set_access_token(tw_access_token, tw_access_token_secret)
twapi = tw.API(auth, wait_on_rate_limit=True)


#Getting the followers count, following, number of tweets, and screen name
influencer_collection = pd.DataFrame()
for index, hdl in handle_df.iterrows():
    try:
        user = twapi.get_user(screen_name=hdl['Handles'])
        followers_count = user.followers_count
        following_count = user.friends_count
        num_of_tweets = user.statuses_count
        screen_name = user.screen_name
        #If the Handle has < 100 followers then do not add to the list
        if followers_count < 100:
            continue
        #Form the Tweet Data to be sent to Dataframe
        tweet_data = [{'Influencer': screen_name, 'Follower Count': followers_count, 'Following': following_count, 'Total Tweets': num_of_tweets, 'Verified': user.verified, 'Location': user.location}]
        tempdf = pd.DataFrame(tweet_data)
        influencer_collection = pd.concat([influencer_collection, tempdf])
        influencer_collection = influencer_collection.reset_index(drop=True)
    except Exception as e:
        pass
#Sort based on the Followers and Total Tweets
influencer_collection = influencer_collection.sort_values(by=['Follower Count', 'Total Tweets'], ascending=False)
print(influencer_collection)