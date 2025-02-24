import sys,os,re
from .DouBaoLoginerFieldMixin import DouBaoLoginerFieldMixin
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.MACLoginerSchema import MACLoginerSchema

class DouBaoMACLoginerSchema(DouBaoLoginerFieldMixin,MACLoginerSchema):

  # === create mac subclass fields ===
  def get_before_fill_atom(self):
    # Typed atom
    atom = [
      # load the main content in 60 seconds
      self.atom_factory.createClickable('Popup the login dialog','button[data-testid="to_login_button"',timeout=60),
    ]
    return self.atom_factory.createArray('switch atom',atom)

  def get_fill_atom(self):
    '''
    Typed atom
    Fill the phone number for send sms
    '''
    atom = [
      # wait the form dialog popup in 10 seconds
      self.atom_factory.createInput('Phone number','input[data-testid="login_phone_number_input"]','17607614755',timeout=10),
      self.atom_factory.createChoice('Agree privacy','.semi-checkbox-inner-display',True),
    ]
    return self.atom_factory.createArray('Fill phone number',atom)

  def get_send_atom(self):
    '''
    Typed atom
    Send the sms
    '''
    atom = [
      self.atom_factory.createClickable('Next step','button[data-testid="login_next_button"]'),
    ]
    return self.atom_factory.createArray('Send the sms',atom)

  def get_before_code_atom(self):
    atom = [
      self.atom_factory.createJSCss('Enable the input wrapper','.code-input .semi-input-wrapper',{'pointer-events':'auto'}),
    ]
    return self.atom_factory.createArray('before code',atom)

  def get_code_atom(self):
    '''
    Typed atom
    Fill in the auth code
    Only one character can be entered in the input field at a time
    It will receive a dynamic value
    '''
    return self.atom_factory.createInputChar('Char input','.code-input .semi-input','',1,'replace')
