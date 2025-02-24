from abc import ABC,abstractmethod
from .LoginerSchema import LoginerSchema

class MACLoginerSchema(LoginerSchema,ABC):

  def __init__(self):

    super().__init__()

    # { ArrayAtom } : the behaviors that show the loginer form
    self.before_fill_atom = self.get_before_fill_atom()
    # { ArrayAtom } : the behaviors that fill the form before sending the code
    self.fill_atom = self.get_fill_atom()
    # { ArrayAtom } : the behaviors that send code
    self.send_atom = self.get_send_atom()
    # { ArrayAtom } : the behavior that before input code
    self.before_code_atom = self.get_before_code_atom()
    # { InputAtom } : the behavior that input the code
    self.code_atom = self.get_code_atom()
    # { ArrayAtom } : the behaviors that submit
    self.submit_atom = self.get_submit_atom()
    # { ValueAtom } : the max waiting time for the sms auth code
    self.captcha_valid_period_atom = self.get_captcha_valid_period_atom()

  @abstractmethod
  def get_before_fill_atom(self):
    pass

  @abstractmethod
  def get_fill_atom(self):
    pass

  @abstractmethod
  def get_send_atom(self):
    pass

  def get_before_code_atom(self):
    pass

  @abstractmethod
  def get_code_atom(self):
    pass

  def get_submit_atom(self):
    '''
    @description: some sites submit automatically after input the verify code
    '''
    pass

  def get_captcha_valid_period_atom(self):
    return self.atom_factory.createData('Captcha valid period',5*60)

