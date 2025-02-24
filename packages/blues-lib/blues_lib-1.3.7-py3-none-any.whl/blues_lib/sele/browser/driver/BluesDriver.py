import sys,os,re,abc
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.BluesFilePool import BluesFilePool   

class BluesDriver(metaclass=abc.ABCMeta):

  def __init__(self):
    self.download_dir = BluesFilePool.get_dir_path('browser_download')
    self.arguments = set() 
    self.experimental_options = dict()
    self.executable_path = ''
    self.selenium_driver = None

  @abc.abstractmethod
  def set_selenium_driver(self):
    '''
    @description : Set driver's driver package
    '''
    pass

  @abc.abstractmethod
  def set_executable_path(self):
    '''
    @description : Set driver's executable path
    '''
    pass

  @abc.abstractmethod
  def set_arguments(self):
    '''
    @description : Set standard browser parameters
    '''
    pass

  @abc.abstractmethod
  def set_experimental_options(self):
    '''
    @description : Set browser extension parameters by selenium
    '''
    pass

  @abc.abstractmethod
  def get(self):
    '''
    @description : Get the web driver instance
    '''
    pass
