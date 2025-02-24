import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.AccountLoginerSchema import AccountLoginerSchema

class MoshuAccountSchema(AccountLoginerSchema):
  
  # === create the base fields ===
  def create_log_in_atom(self):
    self.log_in_atom = self.atom_factory.createURL('Log in url','https://open.ai-moshu.cc/#/')

  def create_proxy_atom(self):
    config = {
      'scopes': ['.*ai-moshu.cc.*'],
    }
    self.proxy_atom = self.atom_factory.createData('proxy config',config)

  def create_cookie_filter_atom(self):
    config = {
      'url_pattern':'/user/get_app_detail',
      'value_pattern':None
    }
    self.cookie_filter_atom = self.atom_factory.createData('cookie filter config',config)
  
  # === create the account subtype fields ===
  def create_switch_atom(self):
    atom = [
      self.atom_factory.createClickable('Open the dialog','.click_new'),
      self.atom_factory.createClickable('Toggle to login tab','.protocol_tabs_box .protocol_tabs:last-child'),
    ]
    self.switch_atom = self.atom_factory.createArray('switch atom',atom)

  def create_fill_atom(self):
    atom = [
      self.atom_factory.createInput('name','input[name=user_name]','17607614755'),
      self.atom_factory.createInput('password','input[name=password]','Langcai10.'),
    ]
    self.fill_atom = self.atom_factory.createArray('fill atom',atom)

  def create_submit_atom(self):
    atom = [
      self.atom_factory.createClickable('submit','.login_but'),
    ]
    self.submit_atom = self.atom_factory.createArray('submit atom',atom)

