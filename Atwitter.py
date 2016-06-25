import tweepy
from tweepy import OAuthHandler
import MySQLdb
import time
api = None
cursor = None
db =None
def log_in ():
    global api
    #logging in to twitter
    access_token = "1368859004-4UCKl3RTLlIYPRZAFArtVLbYa6qRUsXqWfshNHD"
    access_token_secret = "BzLPXiZhyLhLpoWqlhHzJgUOQrUqSJCWxSqO280x2gZMK"
    consumer_key = "wbSeyx09O89lJBugKGavu5XrK"
    consumer_secret = "R6mXO95Ch6H5eY14bARL4hb1cDp2hMCjF1SZq9dDkFXE38L0ee"
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
def connect_database():
    global cursor,db
    # Open database connection
    db = MySQLdb.connect("127.0.0.1", "admin", "admin", "twitter_bot")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
#this function tells wheather supplied handle is a valid twitter handle or not
# 0 -> not a valid use ; 1 -> valid user
def validating_handle(handle):
    global api
    if api == None :
        log_in()
    try:
        api.get_user(screen_name=handle)
    except tweepy.error.TweepError as e:
    #    print ("IN EROR")
        return 0
    return 1
def adding_handels_to_database(handles,whatsapp_id):
    global cursor,db
    if cursor == None :
        connect_database()
    for handle in handles :
        # try :
        #     last_tweet_id = getting_last_tweet_id(handle)
        # except tweepy.error.TweepError :
        #     send_message("The supplied handle %s is not valid" % handle )
        #     del handels[index]
        #     continue
        #print (last_tweet_id)
        last_tweet_id = getting_last_tweet_id(handle)

        query1 = "INSERT INTO twitter(handles,Last_Tweet_ID,Subscribers) values ('%s','%s','%s') " % (handle,str(last_tweet_id),whatsapp_id+",")

        try :
            #if it executes it means the handle was not present previously
            cursor.execute(query1)
            db.commit()
        except :
            # if this executes then it means handle was present and only to whastapp id will be added
            query_get_subscribers = "SELECT Subscribers FROM twitter WHERE handles= '%s' " % (handle)
            try :
                cursor.execute(query_get_subscribers)
                subscriber_string = cursor.fetchone()[0]
                db.commit()
            except:
                db.rollback()
                return
            subscriber_list = subscriber_string.split(',')
            try :  #removing NONE type entries from the list
                subscriber_list = filter(None,subscriber_list)
            except :
                pass
            subscriber_list.append(whatsapp_id)
            subscriber_list = list(set(subscriber_list))  #dealing with duplicate subscriber entries
            subscriber_string = ",".join(subscriber_list)
            query3 = "UPDATE twitter SET Last_Tweet_ID='%s',Subscribers='%s' WHERE handles='%s' " % (str(last_tweet_id) , subscriber_string , handle)
            try :
                cursor.execute(query3)
                db.commit()
            except :
                db.rollback()
                return
def getting_last_tweet_id(twitter_handel):
    global api
    if api == None :
        log_in()
    try :
        last_tweet = api.user_timeline(screen_name=twitter_handel, count=1)
        last_tweet_id = (last_tweet[0].id)
        return last_tweet_id
   # except tweepy.error.TweepError:
    except :
        pass
def saving_new_tweets() : # this function gets handles and last tweet id from database
    global cursor,db
  #  print ("In saving new tweet")
    if cursor == None :
        connect_database()
    query = "SELECT handles FROM twitter WHERE flag = '%d' "   % (0)  #getting all the hanels with flag 0 i.e. need to refresh the tweet
    try :
        cursor.execute(query)
        db.commit()
        # Fetch all the rows in a list of lists.
        handle_list = cursor.fetchall()
    except :
        db.rollback()
        print ("Unable to fetch tweets")
        return
    for handle in handle_list :
        query_last_tweet_id = "SELECT Last_Tweet_ID FROM twitter WHERE handles = '%s' " % handle[0]
        try :
          cursor.execute(query_last_tweet_id)
          db.commit()
        except :
            db.rollback
            print ("Unable to get last tweet id")
        last_id = cursor.fetchone()[0]
        twitter(handle[0],last_id)
def twitter(handle , last_id):
    global api
    if api == None :
        log_in()
    # while i < len(twitter_handels):
    #     user_data.append({'screen_name': 'xyz', "last_tweet_id": 123})
    #     user_data[i]['screen_name'] = twitter_handels[i]
    #     i += 1
    # for user in user_data:
    #     last_tweet = api.user_timeline(screen_name=user["screen_name"], count=1)
    #     user['last_tweet_id'] = last_tweet[0].id
    while True :
        try :
            new_tweets = api.user_timeline(screen_name=handle, since_id=last_id,)
            break
        except tweepy.error.TweepError:
            print ("Tweepy limit reached : Waiting for 15 minutes")
            time.sleep(900)
    tweets_text = []
    for tweet in new_tweets:
        tweets_text.append(tweet.text)
    message = "\n".join(tweets_text)
    #print (message)
    try :
        new_last_id = new_tweets[0].id
      #  print ("id changed")
                # print ("Latest tweets of " + user['screen_name'] + " are as follows : \n" + message)
                # send_message ("Latest tweets of " + user['screen_name'] + " are as follows : \n" + message)
            # except IndexError:
            #     print ("Index error")
            #     pass
    except :
        new_last_id = last_id # no new tweets
    if new_last_id == last_id :
        flag = 0
    else :
        flag = 1
   # print flag
    query = "UPDATE twitter SET Last_Tweet_ID='%s',tweets='%s',flag='%d' WHERE handles = '%s' " % (new_last_id , message ,flag, handle)
    try :
        cursor.execute(query)
        db.commit()
    except :
        db.rollback()
        print ("Unable to add new tweets to the database")
        return
 #   adding_new_tweets_to_database(handle,new_last_id,message)
    # print ("Now I will be sleeping for 100 secs")
    # time.sleep(100)
    # print ("I woke up")
def sending_tweets():
    global cursor,db
    if cursor == None :
        connect_database()
    #getting handles with flag = 1
    query = "SELECT * FROM twitter WHERE flag = 1 "
    try :
        cursor.execute(query)
        list_rows = cursor.fetchall()
        db.commit()
    except :
        db.rollback()
        print ("Unable to get flag from handles with new tweets")
        return
    if list_rows != () :
        dict_list = []
        i=0    #to keep track of dict_list index
      #  print list_rows
        for row in list_rows :
            #dict_list.append({'whatsapp_id':None , 'msg' : None})
            subscribers_string = row[4]
            handle = row[0]
            #print handle
            # changing flag back to 0 and removing the tweets
            query = "UPDATE twitter SET tweets='' , flag=0 WHERE handles = '%s' " % handle
            try :
                cursor.execute(query)
                db.commit()
            except :
                print ("Unable to change flag and tweets")
                db.rollback()
            #print ("Query executed")
            tweets =  row[1]
            subscriber_list = subscribers_string.split(',')
            # filetering subscriber list for blank entries
            try :
                subscriber_list = filter(None,subscriber_list)
            except :
                pass
            #print subscriber_list
            msg = "Following are lastest tweets from *%s* :\n%s" % (handle,tweets)
            #print ("Following are latest tweets from *%s* :\n %s" % (handle,tweets) )
            for subscriber in subscriber_list :
                dict_list.append({'whatsapp_id': None, 'msg': None})
                dict_list[i]['whatsapp_id'] = subscriber
                dict_list[i]['msg'] = msg
                i+=1
        return dict_list
    else :
        return 0