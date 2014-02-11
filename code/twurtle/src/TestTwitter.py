# TestTwitter.py (c) 2013 @whaleygeek

import sys
import time
from twitter import Twitter
from twitter import RFC822Writer
  
def showUser(user):
  # show the user name on a status screen
  print "user:" + user
  
def showTweet(text):
  print "tweet:" + text
  

BATCH_SIZE = 50 
tw = Twitter()
tw.start()


while True:
  print "waiting for API"
  while True:
    remaining = tw.timeUntilNextUse()
    if (remaining > 0):
      print "waiting:" + str(int(remaining))
      time.sleep(1)
    else:
      break

  print "reading tweets"
  n = tw.read(BATCH_SIZE)
  
  print "candidates:" + str(n) + "/" + str(BATCH_SIZE)
  
  # append in reverse order so that newest are at end of file
  print "appending to tweet file"
  w = RFC822Writer("tweets.txt")
  w.start()
  for i in range(n-1,-1,-1):
    item = tw.get(i)
    w.write(item)
  w.finished()
  
  # show them on the screen in reverse order
  for i in range(n-1,-1,-1): # backwards from n-1 to 0
    item        = tw.get(i)
    id          = item["id"]
    screen_name = item["screen_name"]
    name        = item["name"]
    text        = item["text"]
    
    showUser(screen_name)
    showTweet(text)
      
      
# END


