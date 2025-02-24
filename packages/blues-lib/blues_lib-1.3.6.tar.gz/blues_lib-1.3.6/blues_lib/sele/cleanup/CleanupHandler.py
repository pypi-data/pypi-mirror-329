import sys,os,re
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))

class CleanupHandler(ABC):

  def __init__(self):
    '''
    The abstract class of handlers 
    '''
    self._next_handler = None
  
  def set_next(self,handler):
    '''
    Set the next handler
    Parameter:
      handler {Handler} : the next handler
    Returns 
      {Handler} 
    '''
    self._next_handler = handler
    return handler

  def handle(self,request):
    '''
    The full cleanup handlers chain
    Parameters:
      request {dict} : 
        - browser {Browser}
        - material {Material}
        - log {dict}
          - pub_platform {str} : the publish platform
          - pub_channel {str} : the publish channel
        - validity_days {int} : number of days to retain data
    Returns 
      {None} : don't care the return value
    '''
    self.resolve(request)
    # It's a pipeline, don't stop, go throght all handlers
    if self._next_handler:
      self._next_handler.handle(request)

  @abstractmethod
  def resolve(self,data):
    '''
    This method will be implemented by subclasses
    '''
    pass


