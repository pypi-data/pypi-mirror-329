import sys,os,re
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from atom.AtomFactory import AtomFactory

class LoginerSchema(ABC):

  def __init__(self):

    self.atom_factory = AtomFactory()

    # { URLAtom } : the value atom of loginer page's url
    self.login_page_url_atom = self.get_login_page_url_atom()
    
    # { URLAtom } : the value atom of logged in page's url
    self.loggedin_page_url_atom = self.get_loggedin_page_url_atom()

    # { ElementAtom } : the loginer page's element selector
    self.login_page_identifier_atom = self.get_login_page_identifier_atom()

    # { DataAtom } : the verify login status and save http cookies
    self.max_login_waiting_time_atom = self.get_max_login_waiting_time_atom()

    # { DataAtom } : the value atom of proxy config
    self.proxy_config_atom = self.get_proxy_config_atom()

    # { DataAtom } : the value atom of cookie filter config
    self.cookie_filter_config_atom = self.get_cookie_filter_config_atom()

  # === Create the base required fields
  def get_login_page_url_atom(self):
    return None

  def get_loggedin_page_url_atom(self):
    return None

  def get_login_page_identifier_atom(self):
    # If the web will redirect after login, don't need to set this element
    return self.atom_factory.createElement('notset','')

  def get_max_login_waiting_time_atom(self):
    # At least, to wait the http response to save cookies
    return self.atom_factory.createData('Wait for 10 seconds to confirm the login status',10)

  def get_proxy_config_atom(self):
    return None

  def get_cookie_filter_config_atom(self):
    return None
  