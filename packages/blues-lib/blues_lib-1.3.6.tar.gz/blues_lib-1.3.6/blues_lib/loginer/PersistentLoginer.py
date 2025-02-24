import sys,os,re
from abc import ABC,abstractmethod
from .Loginer import Loginer
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BluesProxyChrome import BluesProxyChrome     
from pool.DBTableIO import DBTableIO
from util.BluesURL import BluesURL      
from util.BluesDateTime import BluesDateTime      
from util.BluesConsole import BluesConsole      

class PersistentLoginer(Loginer,ABC):

  def create_browser(self):
    proxy_config = self.schema.proxy_config_atom.get_value()
    cookie_filter_config = self.schema.cookie_filter_config_atom.get_value()
    self.browser = BluesProxyChrome(proxy_config,cookie_filter_config)
    
  def after_verify(self):
    self.save_cookies()
    self.quit()

  def save_cookies(self):
    BluesDateTime.count_down({
      'duration':10,
      'title':'Wait 10 seconds after jumping to the login page to ensure that the necessary interface completes the request'
    })
    cookie_file = self.browser.save_cookies()
    if cookie_file:
      BluesConsole.success('The cookie has been saved to %s successfully' % cookie_file)
    else:
      BluesConsole.error('The cookie failed to be saved')