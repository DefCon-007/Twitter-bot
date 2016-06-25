import Awhatsapp
import Atwitter
import time
import thread
from KThread import *
flag = 1

def f1() :
    global flag
    while True :
        while flag :
            Awhatsapp.checking_new_message()
def f2() :
    global flag
    while True :
        Atwitter.saving_new_tweets()  # this function checks for new tweets
        returned_list = Atwitter.sending_tweets()   # if it returns 0 , then no new tweets were found
        print returned_list
        if returned_list != 0:
            flag = 0
            #A.kill()
          #  print ("Successfully killed process")
            for element in returned_list:
             #   print element['whatsapp_id']
              #  print ("Inside For loop")
                while True :
                    try :
                        Awhatsapp.selecting_from_recent_contact(element['whatsapp_id'])
                        Awhatsapp.send_message(element['msg'])
                        break
                    except :
                        #print "IN except"
                        pass
           # A.start()
            flag =1
        time.sleep(10)
# thread.start_new_thread(f1,())
# thread.start_new_thread(f2,())
A= KThread(target=f1)
B= KThread(target=f2)
A.start()
B.start()
# f1()
# def a1():
#     print "in a1"
#     # while True :
#     #     pass
#     print "Func stopped"
# def b1():
#     print "in b1"
#     global A
#     i=0
#     while i<5 :
#         print i
#         i+=1
#     A.kill()
# A= KThread(target=a1())
# B= KThread(target=b1())
# thread.start_new_thread(a1,())
# thread.start_new_thread(b1,())
#Atwitter.sending_tweets()

# def func():
#   print 'Function started'
#   for i in xrange(1000000):
#     pass
#   print 'Function finished'
#
# A = KThread(target=func)
# A.start()
# for i in xrange(1000000):
#   pass
# A.kill()
# while True :
#     1
#Awhatsapp.selecting_from_recent_contact('mom')

