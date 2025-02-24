import sys,os,re
from functools import wraps
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesConsole import BluesConsole

class MaterialDeco():
  '''
  Only used to the Acter class's resovle method
  '''

  def __init__(self):
    '''
    Create the decorator
    Has no parameters
    '''
    pass

  def __call__(self,func):
    @wraps(func) 
    def wrapper(*args,**kwargs):

      # the handle's second paramter: materials
      handler_self = args[0]
      request = args[1]
      handler_kind = handler_self.kind
      handler_name = type(handler_self).__name__
      
      # execute the wrappered func
      outcome = func(*args,**kwargs)
      
      material = request.get('material')
      if material:
        title = material['material_title']
        values = (handler_kind,handler_name,title)
        BluesConsole.info('Crawler [%s:%s] , material : %s' % values)
      else:
        values = (handler_kind,handler_name)
        BluesConsole.info('Crawler [%s:%s] : no material' % values)
      
      # must return the wrappered func's value
      return outcome

    return wrapper

