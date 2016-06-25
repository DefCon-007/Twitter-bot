from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
from selenium.webdriver.chrome.options import Options
import MySQLdb
import time
import Atwitter

options = Options()
options.add_argument("user-data-dir=browser_data")  # using custom profile where whatsapp is already signed in
Driver = webdriver.Chrome(chrome_options=options)
Driver.get("https://web.whatsapp.com")

# Open database connection
db = MySQLdb.connect("127.0.0.1","admin","admin","twitter_bot" )
# prepare a cursor object using cursor() method
cursor = db.cursor()
#print (1)
def add_user(whastapp_name ) :
    global cursor,db
   # if len(twitter_handles) != 0 :
        # for index,handle in enumerate(twitter_handles) :
        #     import Atwitter
        #     flag = Atwitter.validating_handle(handle) # 0 -> not a valid use ; 1 -> valid user
        #     if flag == 0 :
        #         send_message("The supplied handle %s is not valid" % handle )
        #         del twitter_handles[index]
        # handle_string = "\n".join(twitter_handles)
        # query1 = "INSERT INTO User_Data (Twitter_handles , Whatsapp_ID) VALUES ('%s' , '%s')" % (handle_string, whastapp_name)
        # try :
        #     cursor.execute(query1)
        #     db.commit()
        # except:
        #     send_message("Unable to process request due to server error. Please try after sometime.\nError Code : Adding to server error")
        #     db.rollback()
   # else :
    query2 = "INSERT IGNORE INTO User_Data (Whatsapp_ID) VALUES ('%s')" % (whastapp_name)
    try:
        cursor.execute(query2)
        db.commit()
    except:
        send_message("Error !!! \n Error Code : 401")
        db.rollback()
def adding_handles(handles_list , name) :
    query1 = "SELECT Twitter_handles FROM User_Data WHERE Whatsapp_ID = '%s' " % name
    try :
        cursor.execute(query1)
        saved_handles = cursor.fetchone()[0]  #stores previous handles
        db.commit()
    except :
        db.rollback()
        send_message("Error !!! \n Error Code : 203")
    invalid_handle = ""
   # invalid_handle_index = []
    for handle in handles_list[:] :  # using [:] to get a copy of orginal list
        #print handles_loop
      #  print ("Checking For : " + handle)
        flag = Atwitter.validating_handle(handle)  # 0 -> not a valid use ; 1 -> valid user
        if flag == 0:
          #  send_message("The supplied handle *%s* is not valid" % handle)
          #  print handle
            invalid_handle += handle + ","
            handles_list.remove(handle)
            #invalid_handle_index.append(index)
        else :
            pass
   # print invalid_handle_index
    # for x in invalid_handle_index :
    #     del handles_list[x]
    if invalid_handle[:-1] != "" :
        send_message("The supplied handles : *%s* are not valid" % invalid_handle[:-1])
    handles_list = list(set(handles_list))  # removing duplicate entries
    # filtering list
    try :
        handles_list = filter(None , handles_list)
    except :
        pass
    handle_string = "\n".join(handles_list)  #stores present supplied handles

   # query1 = "INSERT INTO User_Data (Twitter_handles , Whatsapp_ID) VALUES ('%s' , '%s')" % (handle_string, whastapp_name)
   #  try:
   #      cursor.execute(query1)
   #      db.commit()
   #  except:
   #      send_message(
   #          "Unable to process request due to server error. Please try after sometime.\nError Code : Adding to server error")
   #      db.rollback()
    if saved_handles == "" : #this implies no previous handles stored

        query2 = "UPDATE User_Data SET Twitter_handles = '%s' WHERE Whatsapp_ID = '%s'" % (handle_string, name)
        try :
            cursor.execute(query2)
            db.commit()
        except:
            send_message("Error !!! \n Error Code : 301")
            db.rollback()
        Atwitter.adding_handels_to_database(handles_list,name)
    else :
        saved_handles_list = saved_handles.split('\n')
        combined_handles_list = saved_handles_list+ handles_list
        combined_handles_list = list(set(combined_handles_list)) # removing duplicates from the combined
        #filtering new handles list
        try:
            combined_handles_list = filter(None,combined_handles_list)
        except:
            pass
        combined_handles = "\n".join(combined_handles_list)
        query3 = "UPDATE User_Data SET Twitter_handles = '%s' WHERE Whatsapp_ID = '%s'" % (combined_handles, name)
        try :
            cursor.execute(query3)
            db.commit()
        except:
            send_message("Error !!! \n Error Code : 302")
            db.rollback()
        Atwitter.adding_handels_to_database(combined_handles_list,name)
    return handle_string
def checking_new_message():  #here flag=0 -> normal call , flag=1 -> to subscribe , flag=2 -> to unsubscribe
    time.sleep(2)
    i=0
   # print ("func running")
    global Driver,cursor,db
    name = None
    msg = None
    while True :
        try :
            elem_message_list = Driver.find_element_by_css_selector('div.unread.chat')
            elem_message_list.click()
          #  print ("Inside try ")
            break
        except :
          #  print ("Inside Except")
            return
            pass
   # elem_message_list.click()
    #getting sender name and latest message
    header = Driver.find_element_by_css_selector('header.pane-header.pane-chat-header')
    elem_div_name_header = header.find_element_by_css_selector("div.chat-main")
    name = elem_div_name_header.find_element_by_css_selector("span.emojitext.ellipsify").text
    messsages_div = Driver.find_elements_by_css_selector('div.message.message-chat.message-in')
    message_text = messsages_div[len(messsages_div) - 1].find_element_by_css_selector('span.emojitext.selectable-text')  # getting the last message of the received messages
    msg = message_text.text
    #selecting_from_recent_contact("9784830733")  # making current active chat inactive after reading the message
    # try :
    #     # index = getting_index(name)
    #     query1 = "SELECT * FROM User_Data WHERE Whatsapp_ID = '%s' " % name
    #    # try :
    #     cursor.execute(query1)
    #     print 1
    #   #  user = cursor.fetchone()[0]
    #     db.commit()
    #     # except :
    #     #     send_message("Error !!! \n Error Code : 501")
    # except :
    #     print 2
    # query2 = "SELECT * FROM User_Data WHERE Whatsapp_ID = '%s' " % name
       #  try :
    #    cursor.execute(query2)
       # user = cursor.fetchone()
     #   db.commit()
        # except :
        #     send_message("Error !!! \n Error Code : 502")
#    print ("Flag : " + str(user[2]))
#getting the value of flag
    query2 = "SELECT flag FROM User_Data WHERE Whatsapp_ID = '%s' " % name
    try :
        cursor.execute(query2)
        db.commit()
        flag = cursor.fetchone()[0]
    except :
        add_user(name)
        cursor.execute(query2)
        db.commit()
        flag = cursor.fetchone()[0]
   # print flag
    if (msg.lower() == "subscribe tweets" ) :  #subscribing to the tweets
        subscribe(name)
    elif (msg.lower() == "unsubscribe tweets") :  #unsubscribing to the tweets
        unsubscribe(name)
    elif (msg.lower() == "my subscription") : #sending the name of the subscribed twitter handels
        my_subscription(name)
    elif (msg.lower() == "help") :
        send_message("Send *Subscribe Tweets* to subscribe to Tweets\nSend *Unsubscribe tweets* to unsubscribe tweets\nSend *My Subscription* to know your subsciption")

    elif flag == 1 : # adding handles
        twitter_handels = msg.split(" ")
        try :
            twitter_handels = filter(None,twitter_handels) #removing blank handels
        except :
            pass
        subscribed_handle_list = adding_handles(twitter_handels,name)
        # getting handles
        # query1 = "SELECT Twitter_handles FROM User_Data WHERE Whatsapp_ID = '%s' " % name
        # try:
        #     cursor.execute(query1)
        #     handles_string = cursor.fetchone()[0]
        #     db.commit()
        # except:
        #     send_message("Error !!! \n Error Code : 202")
        #     db.rollback()
        # handles_list = handles_string.split('\n')
        # i = 0
        # subscribed_handel_list = ""
        # for x in handles_list:
        #     i += 1
        #     subscribed_handel_list += (str(i) + ". " + x + "\n")
        if subscribed_handle_list == "" :
            send_message("Sorry none of the handles provided by you were valid.Please try again")
        else :
            # adding serial number to handles list
            i = 0
            handle_list = subscribed_handle_list.split("\n")
            subscribed_handle_list_msg = ""
            for x in handle_list:
                i += 1
                subscribed_handle_list_msg += (str(i) + ". " + x + "\n")
            send_message("Congatulations!!! You have been subscribed to\n" + subscribed_handle_list_msg)
        changing_flag(0,name)
       # user_data[index]["flag"] = 0
    elif (flag == 2):
        if msg == "0":
           # user_data[index]['screen_name'] = []
            query = "UPDATE User_Data SET Twitter_handles = '' WHERE Whatsapp_ID = '%s' " % name
            try :
                cursor.execute(query)
                db.commit()
                send_message("You have been unsubscribed from all the Twitter Handles")
            except :
                send_message("Unable to unsubscribe all Twiiter Handles.\nError Code : 601")
            #####    #####    #####   code to unsub particular handel #####  # ### # # # # # #  #
        else :
            numbers = msg.split(',')
            try :
                numbers = filter(None,numbers)
            except :
                pass
            #getting twiiter handles
            query1 = "SELECT Twitter_handles FROM User_Data WHERE Whatsapp_ID = '%s' " % name
            try:
                cursor.execute(query1)
                handles_string = cursor.fetchone()[0]
                db.commit()
            except:
                send_message("Error unable to get the handles")
                db.rollback()
            handles_list = handles_string.split('\n')
            numbers.sort(key=int , reverse=True)
            if handles_list == ['']:
                send_message("You are not subscribed to any Twitter Handle.Send *Subscribe Tweets* to subscribe.")
            else :
                for num in numbers :
                    num = int(num) -1
                    del handles_list[num]
                handles_string_new = "\n".join(handles_list)
                query2 = "UPDATE User_Data SET Twitter_handles = '%s' WHERE Whatsapp_ID = '%s'" % (handles_string_new, name)
                try :
                    cursor.execute(query2)
                    db.commit()
                    if handles_list == [] :
                        send_message("You have been unsubscribed from all the handles")
                    else :
                        i=0
                        subs_list = ""
                        for x in handles_list:
                            i += 1
                            subs_list += (str(i) + ". " + x + "\n")
                        send_message("You are now subscribed to only following Twitter handels :\n" + subs_list)
                except:
                    send_message("Error : Unable to complete request. Unable to unsubscribe")
                    db.rollback()




        changing_flag(0, name)
        #  user_data[index]["flag"] = 0
        return 0
    else :
        send_message("Incorrect Keyword entered. Send *help* to know more." )

  #  Driver.get("https://web.whatsapp.com")

def subscribe(whatsapp_id) :
    #index = getting_index(whatsapp_id)
    send_message("Please send the twitter handel(without '@') of the person whose tweets you want to get.If you want to subscribe to multiple people just separate their handels with a space.\nEx : *iamvirat srbachhan*\n_Since I validate every handle first(as you are human and destined to make mistakes :P) it may take some time according to the number of handles you provided._")
    #user_data[index]["flag"] = 1
    # query = "UPDATE User_Data SET flag=1 WHERE Whatsapp_ID = '%s' " % whatsapp_id
    # try:
    #     cursor.execute(query)
    #     db.commit()
    # except:
    #     send_message("Error !!! \n Error Code : 102")
    #     db.rollback()
    changing_flag(1,whatsapp_id)
    checking_new_message()
def unsubscribe(whatsapp_id) :
  #  index = getting_index(whatsapp_id)
    #user_data[index]['flag'] = 2
# changing flag
#     query1 = "UPDATE User_Data SET flag=2 WHERE Whatsapp_ID = '%s' " % whatsapp_id
#     try:
#         cursor.execute(query1)
#         db.commit()
#     except:
#         send_message("Error !!! \n Error Code : 103")
#         db.rollback()
    changing_flag(2,whatsapp_id)
# getting handles
    query2 = "SELECT Twitter_handles FROM User_Data WHERE Whatsapp_ID = '%s' " % whatsapp_id
    try:
        cursor.execute(query2)
        handles_string = cursor.fetchone()[0]
        db.commit()
    except:
        send_message("Error !!! \n Error Code : 201")
        db.rollback()
    handles_list = handles_string.split('\n')
    i=0
    subscribed_handel_list = ""
    for x in handles_list :
        i+=1
        subscribed_handel_list += (str(i)+". "+x+"\n")
    send_message("You are subscribed to following Twitter handels.\n" + subscribed_handel_list)
    send_message("Send the corresponding Serial number separated by commas to unsubscribe.\nEx : 1,3,5 \nTo unsubscribe all send 0")
    checking_new_message()
def my_subscription(whatsapp_id) :
    # getting handles
    query1 = "SELECT Twitter_handles FROM User_Data WHERE Whatsapp_ID = '%s' " % whatsapp_id
    try:
        cursor.execute(query1)
        handles_string = cursor.fetchone()[0]
        db.commit()
    except:
        send_message("Error !!! \n Error Code : 202")
        db.rollback()
    handles_list = handles_string.split('\n')
    if handles_list == [''] :
        send_message("You are not subscribed to any Twitter Handle.Send *Subscribe Tweets* to subscribe.")
    else :
        i = 0
        subscribed_handel_list = ""
        for x in handles_list:
            i += 1
            subscribed_handel_list += (str(i) + ". " + x + "\n")
        send_message("You are subscribed to following Twitter handels :\n" + subscribed_handel_list)

#this function sends message on whatsapp
def send_message(i):
    message_list = i.split("\n")
    global Driver
    elem_messagebox = Driver.find_element_by_css_selector('div.input-container')  #getting the text field
    #elem_messagebox.send_keys(raw_input("Enter Message : "))  #entering the message
    for message in message_list :
        elem_messagebox.send_keys(message)
        elem_messagebox.send_keys(Keys.SHIFT + Keys.ENTER)
    while True :
        try :
            send_button=Driver.find_element_by_css_selector('button.icon.btn-icon.icon-send.send-container')  #selecting the send button
            send_button.click()  #clicking it
            break
        except selenium.common.exceptions.NoSuchElementException:
            pass
        except selenium.common.exceptions.NoSuchWindowException:
            pass
        except selenium.common.exceptions.ElementNotVisibleException:
            pass

def changing_flag(flag_value , name ) :
    global cursor,db
    # changing flag
    query1 = "UPDATE User_Data SET flag= '%s' WHERE Whatsapp_ID = '%s' " % (flag_value , name)
    try:
        cursor.execute(query1)
        db.commit()
    except:
        send_message("Error !!! \n Error Code : 10%s" % flag_value)
        db.rollback()
def selecting_from_recent_contact(contact_name):
    global Driver
    while True :
        try :
            elem_search_bar = Driver.find_element_by_css_selector('input.input.input-search')
            break
        except selenium.common.exceptions.NoSuchElementException:
            #print ("1")
            pass
        except selenium.common.exceptions.NoSuchWindowException:
           # print ("2")
            pass
        except selenium.common.exceptions.ElementNotVisibleException:
           # print ("3")
            pass
    elem_search_bar.send_keys(contact_name)
    time.sleep(5)
    elem_search_bar.send_keys(Keys.ENTER) #hitting enter to select the first result
