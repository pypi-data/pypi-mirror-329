class DouBaoLoginerFieldMixin():

  # === create base fields ===
  def get_login_page_url_atom(self):
    # Base atom
    return self.atom_factory.createURL('Page URL','https://www.doubao.com/chat/')

  def get_loggedin_page_url_atom(self):
    '''
    @description: set the loggedin's page url {URLAtom}
    '''
    return self.atom_factory.createURL('Homepage url','https://www.doubao.com/chat/')

  def get_login_page_identifier_atom(self):
    return self.atom_factory.createElement('login page ele','button[data-testid="to_login_button"')

  def get_proxy_config_atom(self):
    # Base atom
    config = {
      'scopes': ['.*doubao.com.*'],
    }
    return self.atom_factory.createData('proxy config',config)

  def get_cookie_filter_config_atom(self):
    # Base atom
    config = {
      'url_pattern':'/profile/self',
      'value_pattern':None
    }
    return self.atom_factory.createData('cookie filter config',config)