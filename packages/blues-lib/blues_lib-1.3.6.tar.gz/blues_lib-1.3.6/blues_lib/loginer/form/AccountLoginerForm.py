import sys,os,re
from abc import ABC,abstractmethod
from .LoginerForm import LoginerForm
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.behavior.BehaviorChain import BehaviorChain

class AccountLoginerForm(LoginerForm,ABC):

  def perform(self,browser):
    '''
    Implement the template method
    '''
    self.browser = browser
    self.before_fill() 
    self.fill() 
    self.submit() 
  
  def before_fill(self):
    if self.schema.before_fill_atom:
      handler = BehaviorChain(self.browser,self.schema.before_fill_atom)
      handler.handle()

  def fill(self):
    if self.schema.fill_atom:
      handler = BehaviorChain(self.browser,self.schema.fill_atom)
      handler.handle()

  def submit(self):
    if self.schema.submit_atom:
      handler = BehaviorChain(self.browser,self.schema.submit_atom)
      handler.handle()
