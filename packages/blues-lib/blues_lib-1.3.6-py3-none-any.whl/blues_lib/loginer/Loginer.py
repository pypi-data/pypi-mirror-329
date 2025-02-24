import sys,os,re
from abc import ABC, abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesConsole import BluesConsole        
from util.BluesDateTime import BluesDateTime      

class Loginer(ABC):
  def __init__(self,schema,form):
    # { LoginerSchema } 
    self.schema = schema
    # {LoginerForm}
    self.form = form
    # { BluesChrome }
    self.browser = None
    
  def login(self):
    '''
    Final template method
    '''
    try:
      # create browser
      self.create_browser()

      # open the login page
      self.open()
      
      # fill and submit the form
      self.form.perform(self.browser)

      # verify log in status
      is_login_successful = self.verify()
      if not is_login_successful:
        raise Exception('The login status check has failed.')
      else:
        BluesConsole.success('Log in successfully by %s.' % self.__class__.__name__)
      
      # do something after verify
      self.after_verify()
      
      # always return the browser instance
      return self.browser

    except Exception as e:
      BluesConsole.error('Failed to log in: %s' % e)
      BluesDateTime.count_down({
        'duration':10,
        'title':'Failed to log in,the page will close in 10 seconds, error: %s' % e
      })
      self.quit()
      return None

  @abstractmethod
  def create_browser(self):
    '''
    @description: create a browser for login
    '''
    pass

  def open(self):
    '''
    @description: open the login page
    '''
    login_page_url = self.schema.login_page_url_atom.get_value()
    self.browser.interactor.navi.open(login_page_url)

  def verify(self,scenario='login',current_browser=None):
    '''
    @description: Check whether the login succeeds based on the url link change or login page's element
    @param {str} scenario : the loginer's using scenario
      - login : do login 
      - loggedin : log in page by cookie, using loginer in BluesLoginChrome
    '''
    is_login_successful = False
    browser = current_browser if current_browser else self.browser

    login_page_url = self.schema.login_page_url_atom.get_value()
    loggedin_page_url = self.schema.loggedin_page_url_atom.get_value()
    max_login_waiting_time = self.schema.max_login_waiting_time_atom.get_value()
    login_page_identifier = self.schema.login_page_identifier_atom.get_selector()

    if login_page_identifier:
      # mode1: doesn't redirect after login, wait some seconeds to wait the document refresh
      BluesDateTime.count_down({
        'duration':max_login_waiting_time,
        'title':'Wait %s seconds to make sure the landing page is updated' % max_login_waiting_time
      })
      is_login_successful = not browser.element.finder.find(login_page_identifier)
    else:
      # mode1: redirect after login
      if scenario == 'login':
        # do login success, need to redirect to the home
        is_login_successful = browser.waiter.ec.url_changes(log_in_atom,max_login_waiting_time)
      else:
        # login by cookie, can't redirect, keep stay in the current loggedin page
        is_login_successful = not browser.waiter.ec.url_changes(loggedin_page_url,max_login_waiting_time)

    if is_login_successful:
      return True
    else:
      return False

  def after_verify(self):
    '''
    @description: do something after verify successfully
    '''
    pass

  def quit(self):
    if self.browser:
      self.browser.interactor.navi.quit()
