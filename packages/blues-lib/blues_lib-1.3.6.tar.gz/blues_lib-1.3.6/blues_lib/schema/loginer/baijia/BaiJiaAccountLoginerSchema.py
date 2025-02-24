import sys,os,re
from .BaiJiaLoginerFieldMixin import BaiJiaLoginerFieldMixin
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.AccountLoginerSchema import AccountLoginerSchema

class BaiJiaAccountLoginerSchema(BaiJiaLoginerFieldMixin,AccountLoginerSchema):
  
  # === create the account subtype fields ===
  def get_before_fill_atom(self):
    atom = [
      self.atom_factory.createClickable('switch to account mode','div[class^=btnlogin]'),
    ]
    return self.atom_factory.createArray('switch atom',atom)

  def get_fill_atom(self):
    atom = [
      self.atom_factory.createInput('name','#pass-login-main input[name=userName]','17607614755'),
      self.atom_factory.createInput('password','#pass-login-main input[name=password]','Langcai10.'),
      self.atom_factory.createChoice('agree protocal','#pass-login-main input[name=isAgree]',True),
      self.atom_factory.createChoice('remember me','#pass-login-main input[name=memberPass]',True),
    ]
    return self.atom_factory.createArray('fill atom',atom)

  def get_submit_atom(self):
    atom = [
      self.atom_factory.createClickable('submit','#pass-login-main input[type=submit]'),
    ]
    return self.atom_factory.createArray('submit atom',atom)

