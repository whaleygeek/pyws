# RFC822.py (c) 2013 @whaleygeek
#
# See this for "efficient ways to read files", as the file object is iteratable
#
# http://stackoverflow.com/questions/8009882/how-to-read-large-file-line-by-line-in-python



class RFC822Writer:
  def __init__(self, name):
    self.name = name
    
  def start(self):
    self.file = open(self.name, "at")
    
  def write(self, map):
    for key in map:
      self.file.write(key + ": " + str(map[key]) + "\n")
    self.file.write("\n")
    
  def finished(self):
    self.file.close()
    self.file = None
    
    
class RFC822Reader:
  def __init__(self, name):
    self.name = name
    
  def exists(self):
    try:
      self.file = open(self.name, "rt")
      self.file.close()
      return True
    except:
      return False
      
  def start(self):
    self.file = open(self.name, "rt")
  
  def skip(self, n=1):
    if (n == None or n <= 0):
      return None # nonsense, do nothing
    if (n == 0):
      return 0 # none skipped, but we did it
      
    count = 0
    for line in self.file:
      #print line
      if (line == "\n"): # blank line means end of record
        #print "end of record"
        count += 1
        if (count >= n):
          return count # we skipped this number of whole records
          
    # if we get here, it is eof
    self.finished() # prevent re-reads without re-open
    return None # means we didn't achieve desired result, now at EOF
    
  def read(self):
    map = {}
    for line in self.file:
      if (line == "\n"):
        return map # end of record
      else:
        item = line.split(":", 1)
        try:
          key = item[0]
        except IndexError:
          self.finished() # prevent re-reads without re-open
          return None # malformed record
        try:
          value = item[1]
          value = value.rstrip('\n').strip()
        except IndexError:
          value = None
        map[key] = value
        
    # if we get here it is EOF
    self.finished() # prevent re-reads without reopen
    return None # EOF before whole record retrieved
    
  def finished(self):
    if (self.file != None):
      self.file.close()
      self.file = None
    
    
def testWriter():
  w = RFC822Writer("test.txt")
  m = {"id":1, "name":"david", "age":45}
  w.start()
  w.write(m)
  w.write(m)
  w.write(m)
  w.finished()
  
  
def testReader():
  r = RFC822Reader("test.txt")
  r.start()
  r.skip(1)
  item = r.read()
  r.finished()
  for k in item:
    print k + "=" + item[k]
    
    
if __name__ == "__main__":
  testWriter()
  testReader()  


#END

