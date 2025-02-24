import sys,os,re
from abc import ABC,abstractmethod
sys.path.append(re.sub('test.*','blues_lib',os.path.realpath(__file__)))
from atom.AtomFactory import AtomFactory     
from atom.Atom import Atom
from pool.BluesMaterialIO import BluesMaterialIO

class ReleaserSchema(ABC):
  # pub to which site and channel
  PLATFORM = ''
  CHANNEL = ''

  def __init__(self):
    self.atom_factory = AtomFactory()
    
    # declare atom fields
    # {DataAtom} the material filter conditon
    self.limit_atom = None

    # { URLAtom } the form page
    self.url_atom = None
    # { ArrayAtom } the preview atom list
    self.preview_atom = None
    # { ArrayAtom } the submit atom list
    self.submit_atom = None
    # { ArrayAtom } the modal atom list, should be closed
    self.popup_atom = None
    # { ArrayAtom } the activity atom
    self.activity_atom = None
    
    # create atoms fields
    self.create_fields()
    # create sub atoms fields
    self.create_sub_fields()
  
  def create_fields(self):
    self.create_limit_atom()
    self.create_url_atom()
    self.create_preview_atom()
    self.create_submit_atom()
    self.create_popup_atom()
    self.create_activity_atom()
  
  @abstractmethod
  def create_sub_fields(self):
    pass

  @abstractmethod
  def create_limit_atom(self):
    pass

  @abstractmethod
  def create_url_atom(self):
    pass

  @abstractmethod
  def create_preview_atom(self):
    pass

  @abstractmethod
  def create_submit_atom(self):
    pass

  @abstractmethod
  def create_popup_atom(self):
    pass

  @abstractmethod
  def create_activity_atom(self):
    pass

