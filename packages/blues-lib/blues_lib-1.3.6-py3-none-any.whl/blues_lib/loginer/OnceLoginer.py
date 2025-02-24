import sys,os,re
from abc import ABC,abstractmethod
from .Loginer import Loginer
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BluesStandardChrome import BluesStandardChrome     

class OnceLoginer(Loginer,ABC):
  '''
  @description: In a single login, the Browser instance is returned without saving the cookie
  '''

  def create_browser(self):
    self.browser = BluesStandardChrome()
