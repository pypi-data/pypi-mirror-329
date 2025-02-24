import sys,os,re
from abc import ABC,abstractmethod
from .AISchema import AISchema

class AIQASchema(AISchema,ABC):

  def __init__(self):
    super().__init__()

    # {DataAtom}
    self.size_atom = 100

    # { ArrayAtom }
    self.question_atom = None

    # { ArrayAtom }
    self.submit_atom = None

    # { ArrayAtom }
    self.popup_atom = None

    # { ArrayAtom }
    self.answer_atom = None

    # crete the atom fileds
    self.create_fields()

  def create_fields(self):
    self.create_size_atom()
    self.create_url_atom()
    self.create_question_atom()
    self.create_submit_atom()
    self.create_answer_atom()
    
  
  def create_size_atom(self):
    pass
  
  @abstractmethod
  def create_question_atom(self):
    '''
    The form for input question 
    '''
    pass

  @abstractmethod
  def create_submit_atom(self):
    '''
    Sbumit the question
    '''
    pass

  def create_popout_atom(self):
    pass

  @abstractmethod
  def create_answer_atom(self):
    '''
    The atom for read the answer
    '''
    pass
