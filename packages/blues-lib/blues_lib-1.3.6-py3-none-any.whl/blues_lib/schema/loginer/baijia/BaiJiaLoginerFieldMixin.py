class BaiJiaLoginerFieldMixin():

  # === common fields of BaiJia login ===
  def get_login_page_url_atom(self):
    '''
    @description: set the login's page url {URLAtom}
    '''
    return self.atom_factory.createURL('Log in url','https://baijiahao.baidu.com/builder/theme/bjh/login')

  def get_loggedin_page_url_atom(self):
    '''
    @description: set the loggedin's page url {URLAtom}
    '''
    return self.atom_factory.createURL('Homepage url','https://baijiahao.baidu.com/builder/rc/home')

  def get_login_page_identifier_atom(self):
    '''
    @description: set the css selector of the identifier in the login page{ElementAtom}
    '''
    return self.atom_factory.createElement('Login page identifier','div[class^=btnlogin]')

  def get_max_login_waiting_time_atom(self):
    '''
    @description: set the max login waiting time {DataAtom}
    '''
    return self.atom_factory.createData('Wait for 15 seconds to confirm the login status',15)

  def get_proxy_config_atom(self):
    '''
    @description: set the browser proxy for persistent loginer {DataAtom}
    '''
    config = {
      'scopes': ['.*baijiahao.baidu.com.*'],
    }
    return self.atom_factory.createData('proxy config',config)

  def get_cookie_filter_config_atom(self):
    '''
    @description: set the logged cookie filter patterns for persistent loginer {DataAtom}
    '''
    config = {
      'url_pattern':'/builder/rc/home',
      'value_pattern':None
    }
    return self.atom_factory.createData('cookie filter config',config)
  
