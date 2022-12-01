# twitterTrends
Grabs the current Trending topics on Twitter in the United States
Description:

Sends me text messages for any of the Top 12 trending topics on twitter only if its what Im looking for. I use it 
to help notify me when topics are trending so i can create youtube videos about it while they're in the search aglorithm. 

More will be added soon. I will have it also connect with Google Trends API soon and compare data.

------------------------------------------------------------------------------

Instructions:

pip install the following - 

twilio (Must make an account on Twilio)
tweepy
google-api-python-client

1.Enable Google Sheets as an API on Google's Cloud services (FREE)
Should create and download a key/json. This will be used for Google's sheets. Google sheets will host all your data
and put it in a nice excel sheet

Example: https://docs.google.com/spreadsheets/d/1jjSd_rhlCfZcFSxa7R5OC0ji5fF188_mdW9NjVF5duc/edit?usp=sharing
Column E has all the trends that I wished to recieve a text for

2. Get API Credentials from Twitter as well as Twilio


