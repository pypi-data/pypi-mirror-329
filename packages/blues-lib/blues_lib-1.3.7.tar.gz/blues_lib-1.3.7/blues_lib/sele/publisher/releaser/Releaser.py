import sys,os,re,time
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.behavior.FormBehavior import FormBehavior       
from util.BluesConsole import BluesConsole

class Releaser(ABC):

  def __init__(self,browser,schema):
    self.browser = browser
    self.schema = schema

  def release(self):
    self.prerelease()
    self.submit()

  def prerelease(self):
    self.open()
    self.fill()
    self.preview()

  def open(self):
    url = self.schema.url_atom.get_value()
    self.browser.open(url)

  @abstractmethod
  def fill(self):
    pass

  def preview(self):
    self._fill_field('preview_atom')

  def submit(self):
    self._fill_field('submit_atom')

  def _fill_field(self,atom_field):
    '''
    A general method to fill fields by atoms
    '''
    if not atom_field or not hasattr(self.schema,atom_field):
      return
    
    fill_atom = getattr(self.schema,atom_field)
    if not fill_atom:
      return 

    popup_atom = getattr(self.schema,'popup_atom')
    handler = FormBehavior(self.browser,fill_atom,popup_atom)
    handler.handle()
    BluesConsole.info('Field [%s] filled' % atom_field)


