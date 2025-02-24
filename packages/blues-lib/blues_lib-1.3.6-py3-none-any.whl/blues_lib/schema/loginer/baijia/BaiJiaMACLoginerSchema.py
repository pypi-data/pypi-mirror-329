import sys,os,re
from .BaiJiaLoginerFieldMixin import BaiJiaLoginerFieldMixin

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.MACLoginerSchema import MACLoginerSchema

class BaiJiaMACLoginerSchema(BaiJiaLoginerFieldMixin,MACLoginerSchema):
  
  # === create mac subclass fields ===
  def get_before_fill_atom(self):
    # Typed atom
    atom = [
      # load the main content in 60 seconds
      self.atom_factory.createClickable('Popup the login dialog','div[class^=btnlogin]'),
      self.atom_factory.createClickable('Switch to MAC mode','#pass-login-main .sms-login'),
    ]
    return self.atom_factory.createArray('switch atom',atom)

  def get_fill_atom(self):
    '''
    Typed atom
    Fill the phone number for send sms
    '''
    atom = [
      # wait the form dialog popup in 10 seconds
      self.atom_factory.createInput('Phone number','.pass-form-item-smsPhone input[name=username]','17607614755',timeout=10),
      self.atom_factory.createChoice('Agree privacy','.tang-pass-sms-agreement input[name=smsIsAgree]',True),
    ]
    return self.atom_factory.createArray('Fill phone number',atom)

  def get_send_atom(self):
    '''
    Typed atom
    Send the sms
    '''
    atom = [
      self.atom_factory.createClickable('Next step','.pass-item-timer'),
    ]
    return self.atom_factory.createArray('Send the sms',atom)

  def get_code_atom(self):
    '''
    Typed atom
    Fill in the auth code
    Only one character can be entered in the input field at a time
    It will receive a dynamic value
    '''
    return self.atom_factory.createInput('Char input','.pass-form-item-smsVerifyCode input[name=password]','')

  def get_submit_atom(self):
    '''
    Typed atom
    Submit to login, this site will submit automatically after the auth code are filled
    '''
    atom = [
      self.atom_factory.createClickable('submit button','p[id$=smsSubmitWrapper] .pass-button'),
    ]
    return self.atom_factory.createArray('Submit',atom)


