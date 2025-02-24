import sys,os,re
from abc import ABC,abstractmethod
sys.path.append(re.sub('test.*','blues_lib',os.path.realpath(__file__)))
from atom.AtomFactory import AtomFactory     

class AISchema(ABC):

  def __init__(self):
    self.atom_factory = AtomFactory()

    # { URLAtom}
    self.url_atom = None

  @abstractmethod
  def create_url_atom(self):
    '''
    The form for input question and submit
    '''
    pass
 
