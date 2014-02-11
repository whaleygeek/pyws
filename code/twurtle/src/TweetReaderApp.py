# TweetReaderApp.py (c) 2013 @whaleygeek

import sys
import time
import re
from twitter import Twitter
from twitter import RFC822Writer
from twitter import RFC822Reader
from twitter import StateFile

# CONFIGURATION

# Set this to a screen_name or tag match depending on your requirements
REGEXP_ISCOMMAND = ".*#test3.*"

# number of commands to try to autolist on program start
AUTOLIST_COMMANDS = 20

# The number of tweets to try to read on each call to the Twitter API
# twitter limits this to about 200
BATCH_READ_SIZE = 50 




last_commandidx = 0



def trace(msg):
  pass # print msg
  
def progress(amount, total):
  pass # print str(int(amount)) + "/" + str(int(total))


# Store the last tweet processed in tweets.txt inside state file last_tweet.txt

class LastTweet(StateFile):
  def __init__(self, filename="last_tweet.txt"):
    super(LastTweet, self).__init__(filename)
    
  def read(self):
    m = super(LastTweet, self).read()
    if (m == None):
      return 0
    id = m["id"]
    id = int(id)
    return id
    
  def write(self, id):
    m = {"id":id}
    super(LastTweet, self).write(m)

# The last command index written to command.txt
# this makes it possible to work out how many commands to expect
# in the file without necessarily reading the whole file.

class LastCommand(StateFile):
  def __init__(self, filename="last_command.txt"):
    super(LastCommand, self).__init__(filename)
    
  def read(self):
    m = super(LastCommand, self).read()
    if (m == None):
      return 0
    id = m["id"]
    id = int(id)
    return id
    
  def write(self, id):
    m = {"id":id}
    super(LastCommand, self).write(m)
 
 
def dumpLastFewCommands():  
  global AUTOLIST_COMMANDS  
  global last_commandidx
  last_commandidx = LastCommand().read()
  if (last_commandidx == 0):
    return # nothing to do

  if (last_commandidx > AUTOLIST_COMMANDS):
    num = AUTOLIST_COMMANDS
  else:
    num = last_commandidx
    
  trace("listing last " + str(num) + " commands")
  cr = RFC822Reader("commands.txt")
  idx = 1+ (last_commandidx - num)
  
  cr.start()
  if (idx > 1):
    result = cr.skip(idx-1)
  else:
    result = 0
    
  if (result != None):
    while True:
      c = cr.read()
      if (c == None):
        break # unexpected early EOF
      showCommand(idx, c["screen_name"], c["command"])
      idx += 1
      
  cr.finished()


def waitForApi():
  global tw
  remaining = tw.timeUntilNextUse()
  print "waiting:" + str(int(remaining))
  # wait for the Twitter API to be ready to accept another request.
  # The API will enforce this for us too
  # but this makes sure we can see the waiting progress
  while True:
    remaining = tw.timeUntilNextUse()
    if (remaining > 0):
      progress(60-remaining, 60)
      time.sleep(5)
    else:
      break


def storeTweets(new_tweets):
  # append tweets in reverse order to end of tweets.txt file
  global tw
  trace("appending to tweet file")
  w = RFC822Writer("tweets.txt")
  w.start()
  for i in range(new_tweets-1,-1,-1):
    item = tw.get(i)
    
    # remove newlines, they damage the RFC822 format at the moment
    text = item["text"]
    text = re.sub("\n", "", text)
    item["text"] = text
    
    w.write(item)
  w.finished()
 
  
def processTweets(): 
  # Read any new unprocessed tweets from the tweets.txt file
  # scan them for commands, and append any new commands to commands.txt

  global last_commandidx
  
  # what was the last tweet idx processed from tweets.txt?
  # 0 means nothing has been processed yet
  lt = LastTweet()
  lt_idx = lt.read()
  
  # TODO need to get last_command so that we can print the command
  # numbers on the screen. last_command.txt must be kept in step with
  # command.txt contents for this to work reliably.
  
  # skip to that point in tweets.txt
  trace("skipping to last processed:" + str(lt_idx))
  tr = RFC822Reader("tweets.txt")    
  tr.start()
  
  for i in range(lt_idx):
    if (tr.skip() == None):
      trace("premature end of tweet file")
      return # hit EOF earlier than expected
    
  # if there are any left, we must now process them one by one
  while True:
    tweet = tr.read()
    if (tweet == None):
      tr.finished()
      break
      
    # There is another tweet, filter it for commands
    id          = tweet["id"]
    screen_name = tweet["screen_name"]
    name        = tweet["name"]
    text        = tweet["text"]
    
    if (not isCommand(text)):
      trace("skipping:" + text)
    else:
      trace("storing")
      command = justCommand(text)
      storeCommand(id, screen_name, name, command)
      last_commandidx += 1
      LastCommand().write(last_commandidx)
      showCommand(last_commandidx, screen_name, command)
      
    # update the last tweet index after a successful write
    # this means if we crash, we can always resume from this point
    lt_idx += 1
    lt.write(lt_idx)
  
  
def isCommand(text):
  # work out if this tweet text contains a command or not
  global REGEXP_ISCOMMAND
  
  # Ignore RT anywhere
  if (re.match("RT[ ]+@.+:", text) != None):
    trace("removed RT")
    return False

  # Ignore MT anywhere
  if (re.match("MT[ ]+@.+:", text) != None):
    trace("removed MT")
    return False
  
    
  if (re.match(REGEXP_ISCOMMAND, text) != None):
    return True
  else:
    return False

  
def justCommand(text):
  #trace("before:" + text)
  # strip just the command from this tweet text
  # filter off initial RT:, MT: and other prefixes if possible
  #use re.sub(pattern, replace)
  # can OR together all the replacements
  
  # To make the regexp's easier to write for the end of line condition,
  # we append a single space to the end so it can be used as a terminator
  # in all cases
  text = text + " "

  # hash tags
  STRIP_RE = "#[^ ]+"  
  text = re.sub(STRIP_RE, "", text)  
  
  # screen names
  STRIP_RE = "@[^ ]+"
  text = re.sub(STRIP_RE, "", text)

  # web addresses http and HTTPS
  STRIP_RE = "http[s]*://[^ ]+"
  text = re.sub(STRIP_RE, "", text)
  
  # remove all symbols and spaces, leave just letters and digits
  STRIP_RE = "[^A-Za-z0-9]+"
  text = re.sub(STRIP_RE, "", text)
  
  # finally uppercase it
  text = text.upper()
  
  #trace("after:" + text)
  # hopefully what is left is a command string
  return text  


def storeCommand(id, screen_name, name, command):
  #trace("from:" + screen_name)
  #trace("command:" + command)
  item = {"id": id, "screen_name": screen_name, "name":name, "command":command}
  
  cw = RFC822Writer("commands.txt")
  cw.start()
  cw.write(item)
  cw.finished()
  
def showCommand(idx, screen_name, command):
  print str(idx) + ". (" + screen_name + "): " + command


#-------------------------------------------------------------------------------
# TOP LOOP

# Initial tweets.txt processing in case we crashed and are resuming
# otherwise we have to wait for at least one new tweet to come in
# before we resume fully.

trace("processing any tweets after resume")
if (RFC822Reader("tweets.txt").exists()):
  processTweets()
  
trace("dumping last few commands")
dumpLastFewCommands()
  
tw = Twitter()
tw.start()

while True:
  trace("waiting for API")
  waitForApi()

  trace("reading tweets")
  new_tweets = tw.read(BATCH_READ_SIZE)
  trace("candidates:" + str(new_tweets) + "/" + str(BATCH_READ_SIZE))
  
  if (new_tweets != 0):
    trace("storing tweets")
    storeTweets(new_tweets)
    
    trace("processing tweets")
    processTweets()
    
      
# END


