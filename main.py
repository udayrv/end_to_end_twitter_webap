import tweepy
from textblob import TextBlob
import credentials
import settings
import re
import mysql.connector

def clean_tweet(text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

def deEmojify(text):
    '''Strip all non-ASCII characters to remove emoji characters'''
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None

auth  = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def stream(search_for):
    for status in tweepy.Cursor(api.search_tweets, q = search_for, lang='en').items(100):
        if hasattr(status, "retweeted_status"):  # Check if a tweet is a Retweet
            try:
                #If the tweet is not truncated it won't have the extended_tweet attribute.
                tweet = status.retweeted_status.extended_tweet["full_text"] 
            except AttributeError:
                tweet = status.retweeted_status.text
        else:
            try:
                tweet = status.extended_tweet["full_text"]
            except AttributeError:
                tweet = status.text

        #Extracting required attributes from the status (tweet) object. 
        id_str = status.id_str
        created_at = status.created_at
        text = clean_tweet(deEmojify(tweet))
        sentiment = TextBlob(text).sentiment #Getting the sentiment of a Tweet
        polarity = sentiment.polarity 
        subjectivity = sentiment.subjectivity
        user_created_at = status.user.created_at
        user_location = deEmojify(status.user.location)
        user_followers_count = status.user.followers_count
        longitude = None
        latitude = None
        if status.coordinates:
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]
        retweet_count = status.retweet_count
        favorite_count = status.favorite_count

        #Connecting to Local Database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root2",
            password="password",
            database="TwitterDB",
            charset = 'utf8',
            auth_plugin='mysql_native_password'
        )
        
        #Check if this table exits. If not, then create a new one.
        if mydb.is_connected():
            mycursor = mydb.cursor()
            mycursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_name = '{0}'
                """.format(search_for))
            if mycursor.fetchone()[0] != 1:
                mycursor.execute("CREATE TABLE {} ({})".format(search_for, settings.TABLE_ATTRIBUTES))
                mydb.commit()
            mycursor.close()

        #Writing Data into Database.
        if mydb.is_connected():
            mycursor = mydb.cursor()
            sql = "INSERT INTO {} (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, \
                user_followers_count, longitude, latitude, retweet_count, favorite_count) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(search_for)
            val = (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, \
                user_followers_count, longitude, latitude, retweet_count, favorite_count)
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()
        else:
            print("Database Not Connected")
    #Closing Database connection after writing the data.
    mydb.close()