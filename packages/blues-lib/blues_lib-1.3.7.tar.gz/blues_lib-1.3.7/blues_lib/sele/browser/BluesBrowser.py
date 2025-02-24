import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
# sele
from sele.interactor.Interactor import Interactor  
from sele.element.Element import Element  
from sele.waiter.Waiter import Waiter  
from sele.action.Action import Action  

# script
from sele.script.Script import Script 

# parse
from sele.parser.BluesParser import BluesParser  

class BluesBrowser():

  def __init__(self):
    self.interactor = Interactor(self.driver)  
    self.element = Element(self.driver)  
    self.waiter = Waiter(self.driver)  
    self.action = Action(self.driver)  
    self.script = Script(self.driver)  
    self.parser = BluesParser(self.driver)  

  def open(self,url):
    self.interactor.navi.open(url)
      
  def quit(self):
    self.interactor.navi.quit()

