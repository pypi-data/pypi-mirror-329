import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.QRCodeLoginerSchema import QRCodeLoginerSchema

class ChannelsQRCodeSchema(QRCodeLoginerSchema):

  # === create base fields ===
  def create_log_in_atom(self):
    self.log_in_atom = self.atom_factory.createURL('Login URL','https://channels.weixin.qq.com/login.html')

  def create_verify_wait_period_atom(self):
    self.verify_wait_period_atom = self.atom_factory.createData('verify wait atom',4*60)

  def create_proxy_atom(self):
    # Base atom
    config = {
      'scopes': ['.*qq.com.*'],
    }
    self.proxy_atom = self.atom_factory.createData('proxy config',config)

  def create_cookie_filter_atom(self):
    # Base atom
    config = {
      'url_pattern':'/auth/get_auth_info', #'/post/post_list', # /auth/auth_data
      'value_pattern':None
    }
    self.cookie_filter_atom = self.atom_factory.createData('cookie filter config',config)
  
  # === create mac subclass fields ===
  def create_switch_atom(self):
    return None

  def create_code_atom(self):
    atoms = [
      # the title will be the return dict's key
      self.atom_factory.createFrame('framein','iframe.display','in'),
      self.atom_factory.createShot('shot','img.qrcode'),
      self.atom_factory.createFrame('frameout','','out'),
    ]
    self.code_atom = self.atom_factory.createArray('get shot image',atoms)


