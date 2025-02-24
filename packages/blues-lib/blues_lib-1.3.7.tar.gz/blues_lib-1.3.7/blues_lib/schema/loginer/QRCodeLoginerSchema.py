from abc import ABC,abstractmethod
from .LoginerSchema import LoginerSchema

class QRCodeLoginerSchema(LoginerSchema,ABC):

  def __init__(self):

    super().__init__()

    # { ArrayAtom } : the behaviors that show the loginer form
    self.before_fill_atom = self.get_before_fill_atom()
    # { InputAtom } : the behavior that input the code
    self.code_atom = self.get_code_atom()

  # define the mini steps 
  @abstractmethod
  def get_before_fill_atom(self):
    pass

  @abstractmethod
  def get_code_atom(self):
    pass

