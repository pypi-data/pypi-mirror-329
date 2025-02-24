import sys,os,re,time
from abc import ABC,abstractmethod
from .releaser.ReleaserFactory import ReleaserFactory
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BluesLoginChrome import BluesLoginChrome    
from util.BluesConsole import BluesConsole
from util.BluesDateTime import BluesDateTime

class Publisher(ABC):

  def __init__(self,models,loginer=None):
    # {list<dict>} : {'schema':xxx,'material':xx}
    self.models = models
    # { Loginer } the site's loginer
    self.loginer = loginer
    # { BluesLoginChrome } login auto
    self.browser = None
  
  @abstractmethod
  def accept(self,visitor):
    '''
    Double dispatch with visitor
    '''
    pass

  def accept_test(self,visitor,callback):
    visitor.visit_test(self,callback)

  def publish(self):
    '''
    @description : the final method
    '''
    self.precheck()
    self.login()
    self.__recursive_release()
    self.quit()
  
  def __recursive_release(self):
    models = self.__get_models()
    factory = ReleaserFactory()
    for model in models:
      schema = model['schema']
      releaser = factory.create(self.browser,schema)

      if not releaser:
        BluesConsole.info('No available releaser for channel: %s' % schema.CHANNEL)
        continue

      try:
        releaser.release()
        self.verify(model)
      except Exception as e:
        self.catch(model,e)
      finally:
        BluesDateTime.count_down({'duration':5,'title':'Cleanup after 5 seconds'})
        self.cleanup(model)

  def prepublish(self):
    '''
    @description : the final method
    '''
    self.precheck()
    self.login()
    self.__recursive_prerelease()
    self.quit()

  def __recursive_prerelease(self):
    models = self.__get_models()
    factory = ReleaserFactory()
    for model in models:
      schema = model['schema']
      releaser = factory.create(self.browser,schema)
      if releaser:
        releaser.prerelease()
      else:
        BluesConsole.info('No available releaser for channel: %s' % schema.CHANNEL)

  def __get_models(self):
    return self.models if type(self.models)==list else [self.models]

  def precheck(self):
    if not self.models:
      raise Exception('No available models')

  def login(self):
    self.browser = BluesLoginChrome(self.loginer)

  def quit(self):
    if self.browser:
      self.browser.quit()

  def verify(self,model):
    '''
    Verify whether the publication is successful.
    If the publication is successful and the page jumps, then the publishing button element will not exist.
    '''
    # Use the form page's submit element to make sure weather published succesfully
    schema = model['schema'] 
    material = model['material'] 
    url = schema.url_atom.get_value()
    if self.browser.waiter.ec.url_changes(url,10):
      material['material_status'] = 'pubsuccess'
    else:
      material['material_status'] = 'pubfailure'

  def catch(self,model,error):
    material = model['material'] 
    material['material_status'] = 'pubfailure'
    BluesConsole.error(error,'Publish failure')
    
  def cleanup(self,material):
    pass
  
