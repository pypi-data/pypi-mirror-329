from abc import ABC,abstractmethod
from .LoginerSchema import LoginerSchema

class AccountLoginerSchema(LoginerSchema,ABC):

  def __init__(self):

    # invoke the parent's consrctor
    super().__init__()

    # { ArrayAtom } : the behaviors that show the loginer form
    self.before_fill_atom = self.get_before_fill_atom()

    # { ArrayAtom } : the behaviors that fill the form
    self.fill_atom = self.get_fill_atom()

    # { ArrayAtom } : the behaviors that submit
    self.submit_atom = self.get_submit_atom()

  # define the mini steps 
  @abstractmethod
  def get_before_fill_atom(self):
    pass

  @abstractmethod
  def get_fill_atom(self):
    pass

  @abstractmethod
  def get_submit_atom(self):
    pass

