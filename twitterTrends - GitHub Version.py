import tweepy
from datetime import date, datetime
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials 
from googleapiclient.discovery import build
from Text import SendText
from time import sleep

#-------Google Sheets API Info Below
SERVICE_ACCOUNT_FILE = 'your_json_file_goes_here.json' #json File should be in the same folder as this Python Script.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1jjSd_rhlCfZcFSxa7R5OC0ffds3fF188_mdW9NjVF5duc' 


service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

#--------                  Twitter API Info Below


API_Key = " "
API_Key_Secret = " "
Access_Token = " "
Access_Token_Secret = " "

auth = tweepy.OAuthHandler(consumer_key=API_Key, consumer_secret=API_Key_Secret)
auth.set_access_token(Access_Token, Access_Token_Secret)
api=tweepy.API(auth)

def GrabAPI_Trends(trends):
        # Call the Sheets API
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range='twitterData!E2:E100').execute()
        values = result.get('values', []) #Pulls the list into a list of list
        return (values)

#Vars and List Go Here
US_WOEID = "23424977" #Trend code for the United States; Used for Twitter's API
Trend_Result = api.get_place_trends(US_WOEID)
Row = 2
MyTrends = [] #Used as a list for trends we're personally interested in.
Reset = 0
CurrentTrends = [] #Useless atm, may delete later
TrendsWeKnow = [] #For trends that notifications have already been sent out for
today = date.today()
time = datetime.now()
time = time.strftime("%H:%M:%S")
print (time)
print (time[0:5])

print ('Starting at ', time)




#Need this so the bot will know when to reset certain data at 12 at night
request = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID, 
			range = 'twitterData!F'+str(Row), valueInputOption='USER_ENTERED', body={'values': [[str(today)]]}).execute()
request = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID, 
			range = 'twitterData!F3', valueInputOption='USER_ENTERED', body={'values': [[str(time)]]}).execute()

def Yesterday(): #Might delete later
	result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range='twitterData!F2:F2').execute()
	result = [item for items in (result.get('values')) for item in items]
	return (str(result[0]))


MyTrends = GrabAPI_Trends(MyTrends) #Comes back as a list within list
MyTrends = [item for items in MyTrends for item in items] #Removing the list that came back as a list within a list, and just making it one list
#print (MyTrends)


#for trend in Trend_Result[0]['trends']:
#	CurrentTrends.append(trend['name'].lower())

def SubString(string, list):
	for i in list:
		if i in string:
			return True

def ClearColumn(columnLetter): #Used to clear data every day so we can get fresh notifications
	request = service.spreadsheets().values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='twitterData!' + columnLetter +'2:' + columnLetter + '400').execute()

while True:
	Trend_Result = api.get_place_trends(US_WOEID) #Pulls the Top 50 Trends. 
	sleep(300) #So it doesn't send to many request frequently, we have it paud for 5 minutes. May shorten it later
	Reset += 1 #Used for faster API refresh as a var; Not completed tho. Will be used for the Reset "if" statement all the way at the bottom
	TrendNum = 1 #So we know what number a topic is trending as in terms of rank.
	print ('')
	print ('Reset: ', Reset )
	print ('Refreshing in 5 Minutes')
	print ('')
	for trend in Trend_Result[0]['trends'][0:12]:
	#print (trend) #Print this to get the whole list of whats trending in the US currently. It'll be neat.
		print (str(TrendNum) + '. Trending: ' + trend['name'] + ',', 'Tweets: ',trend['tweet_volume'])
		TrendNum += 1
		if trend['name'] not in TrendsWeKnow: #So we dont send out the same notifications
			if trend['name'].lower() in MyTrends or SubString(trend['name'].lower(), MyTrends): #Checks our personal list and see if any of the strings match up with whats trending, and if its what we're interested in.. Even if its a portion of the word
				TrendsWeKnow.append(trend['name'])
				request = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID,
							 range = 'twitterData!A'+ str(Row), valueInputOption='USER_ENTERED', body={'values': [[TrendNum]]}).execute()
				request = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID,
							 range = 'twitterData!B'+ str(Row), valueInputOption='USER_ENTERED', body={'values': [[trend['name']]]}).execute()
				request = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID, 
						range = 'twitterData!C'+str(Row), valueInputOption='USER_ENTERED', body={'values': [[str(today)]]}).execute()
				request = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID, 
						range = 'twitterData!D'+str(Row), valueInputOption='USER_ENTERED', body={'values': [[trend['tweet_volume']]]}).execute()
				Row += 1
				TextMessage = trend['name'] + ' is Trending. Here is the Link: ' + trend['url']
				SendText(TextMessage)
				#print ('Text Sent')

	#else: 
	#	print ('not time yet')

	if Reset > 200:
		today = date.today()
		request = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID, 
			range = 'twitterData!F2:F2', valueInputOption='USER_ENTERED', body={'values': [[str(today)]]}).execute()
		Row = 2
		Reset = 0 #Not used yet
		ClearColumn('A')
		ClearColumn('B')
		ClearColumn('C')
		ClearColumn('D')
		TrendsWeKnow.clear()
		MyTrends.clear()
		MyTrends = GrabAPI_Trends(MyTrends) #Comes back as a list within list
		MyTrends = [item for items in MyTrends for item in items] #Removing the list that came back as a list within a list, and just making it one list
		#print (MyTrends)
		print ('Refreshing Data for the new Day')





print (TrendsWeKnow, Row)
