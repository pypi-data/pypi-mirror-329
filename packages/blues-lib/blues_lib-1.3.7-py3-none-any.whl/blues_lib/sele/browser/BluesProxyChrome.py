import sys,os,re,json
from seleniumwire.utils import decode
from .BluesBrowser import BluesBrowser
from .BluesCookie import BluesCookie 
from .driver.BluesChromeProxyDriver import BluesChromeProxyDriver   
from .driver.proxy.ProxyMessage import ProxyMessage    
from .driver.proxy.ProxyMessageVisitor import ProxyMessageVisitor     
from .driver.proxy.ProxyCookieVisitor import ProxyCookieVisitor      

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesFiler import BluesFiler  
from util.BluesConsole import BluesConsole   

class BluesProxyChrome(BluesBrowser,BluesCookie):
  def __init__(self,proxy_config=None,cookie_config=None):
    '''
    Create a proxy browser instance

    Parameter:
    proxy_config {dict} : the selenium-wire's standard config
      The attributes are added to the driver object
      {
        'scopes':['.*baidu.com.*'],
        'request_interceptor': lambda request, 
        'response_interceptor':lambda request,response,
      }
    cookie_config {dict} : the cookie's filter pattern
      {
        'url_pattern': 'abc/efg', # the request url regexp pattern
        'value_pattern': 'a=b', # the cookie value's regexp pattern
      }
    '''
    self.driver = BluesChromeProxyDriver().get()
    self.__proxy_config = proxy_config
    self.__cookie_config = cookie_config
    self.__set_proxy()
    super().__init__()

  def __set_proxy(self):
    '''
    Add the standard selenium-wire config to the driver isntance
    '''
    if not self.__proxy_config:
      return
    for key,value in self.__proxy_config.items():
      setattr(self.driver,key,value)

  def get_messages(self):
    proxy_message = ProxyMessage(self.driver.requests)
    return proxy_message.accept_message_visitor(ProxyMessageVisitor())

  def get_cookies(self):
    cookie_message = ProxyMessage(self.driver.requests)
    return cookie_message.accept_cookie_visitor(ProxyCookieVisitor(self.__cookie_config))

  def save_messages(self,file=''):
    messages = self.get_messages()
    file_path = file if file else self.__get_default_file('json')
    return BluesFiler.write_json(file_path,messages)

  def save_cookies(self,cookie_file=''):
    cookies = self.get_cookies()
    if not cookies:
      BluesConsole.info('No matched cookie by: %s' % self.__cookie_config)
      return None
    print('cookies',cookies)
    return self.write_cookies(cookies,cookie_file)
