# GenericDynamicProxy.py  (c) 2013 @whaleygeek
# A generic function call proxy for groups of classes
#
# Create an instance of this class that wraps multiple similar class instances.
# Then call any method on this proxy class, with any parameters, and it
# will dispatch in turn to each instance.
#
# This makes it possible for you to have a collection of similar classes
# that all implement the same methods, wrap them in a GenericDynamicProxy(), and
# then call any method of GenericDynamicProxy - the proxy then calls in turn that
# method on all inner instances. It is generic because when you add new
# methods to the inner instances, you don't have to add new methods to
# this wrapper class, it just "works it out live" for you.
#
# Note, if the underlying instance does not have a suitable method signature
# to match, a NameError will occur as you would expect.
#
# see:
# http://rosettacode.org/wiki/Respond_to_an_unknown_method_call#Python
# http://stackoverflow.com/questions/3061/calling-a-function-from-a-string-with-the-functions-name-in-python

class GenericDynamicProxy():
  def __init__(self, instances):
    self.instances = instances
    
  def __getattr__(self, fname):
    # return a proxy function that will call fname(args) on all instances 
    def method(*args, **kwargs):
      for i in self.instances:
        m = getattr(i, fname)
        m(*args, **kwargs)
    return method    
  

class Test1():
  def __init__(self, name):
    self.name = name
    
  def say(self, msg=""):
    print(self.name + ":" + msg)
    
  def repeat(self, msg, times):
    for i in range(times):
      print(self.name + ":" + msg)
      
      
class Test2():
  def __init__(self, name):
    self.name = name
    
  def say(self, msg=""):
    print(self.name + ":" + msg)
    
  # note, if repeat not defined, will get NameError as expected
  def repeat(self, msg, n):
    pass
    
    
def test():
  #an array of instance objects
  instances=[Test1("one"), Test2("two")]
  
  g = GenericDynamicProxy(instances)
  g.say("hello")
  g.repeat("hi", 5)
  
if __name__ == "__main__":
  test()
  
  

# END

