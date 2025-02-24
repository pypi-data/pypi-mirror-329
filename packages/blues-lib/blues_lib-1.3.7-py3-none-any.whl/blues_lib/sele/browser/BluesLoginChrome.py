import sys,os,re
from .BluesCookie import BluesCookie    
from .BluesStandardChrome import BluesStandardChrome   

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesConsole import BluesConsole   
from util.BluesDateTime import BluesDateTime      

class BluesLoginChrome(BluesStandardChrome,BluesCookie):
  '''
  This class is used exclusively to open pages that can only be accessed after login
  There are three ways to complete automatic login:
    1. Login by a cookie string
    2. Login by a cookie file path
    3. Login by the BluesLoginer class
  '''
  
  # Maximum relogin times
  max_relogin_time = 1

  def __init__(self,loginer):
    '''
    Parameter:
      url {str} : the url will be opened
      loginer_or_cookie {Loginer|str} : 
        - when as str: it is the cookie string or local cookie file, don't support relogin
        - when as Loginer : it supports to relogin
      anchor {str} : the login page's element css selector
        some site will don't redirect, need this CS to ensure is login succesfully
    '''
    super().__init__()
    
    # {LoginerSchema} : three kinds of mode, use schema
    self.loginer = loginer

    # {int} : relogin time
    self.relogin_time = 0

    # login
    self.__login()
    
  def __login(self):
    # read cookie need get the domain from the url
    login_page_url = self.loginer.schema.login_page_url_atom.get_value()
    self.open(login_page_url)

    # read the cookie
    cookies = self.read_cookies()
    if cookies and self.__login_with_cookies(cookies):
      BluesConsole.success('Success to login by the cookie')
      return 

    BluesConsole.info('Fail to login by the cookie, relogin...')
    self.__relogin()

  def __login_with_cookies(self,cookies):
    # add cookie to the browser
    self.interactor.cookie.set(cookies) 
    # Must open the logged in page ,Otherwise, you cannot tell if you have logged in
    loggedin_page_url = self.loginer.schema.loggedin_page_url_atom.get_value()
    self.open(loggedin_page_url)

    # Check if login successfully
    return self.loginer.verify('loggedin',self)

  def __relogin(self):
    if self.relogin_time>=self.max_relogin_time:
      BluesConsole.error('Login failed, the maximum number of relogins has been reached.')
      return

    self.relogin_time+=1
    
    # Relogin and save the new cookies to the local file
    BluesConsole.info('Relogin using the %s' % type(self.loginer).__name__)
    self.loginer.login()

    # Reopen the page using the new cookies
    self.__login()

