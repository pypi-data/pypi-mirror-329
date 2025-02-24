import sys,os,re,copy

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))

from sele.behavior.Behavior import Behavior
from atom.composite.ArrayAtom import ArrayAtom
from entity.STDOut import STDOut

# only need Array
from sele.behavior.composite.Array import Array  

# decorator
from sele.behavior.deco.BehaviorDeco import BehaviorDeco

class Brief(Behavior):

  @BehaviorDeco(True,True)
  def resolve(self):
    '''
    It's a Behavior subclass
    It deal a atom list
    '''
    if self.kind!='brief':
      return False 
    
    # get data unit's parent selector
    if not self.selector:
      return STDOut(501,'selector is missing')
  
    if type(self.value)!=ArrayAtom:
      return STDOut(502,'value type is not ArrayAtom')
    
    # query_all unit elements
    unit_elements = self.browser.waiter.querier.query_all(self.selector)
    if not unit_elements:
      return STDOut(503,'selector (%s) element is missing' % self.selector)
    
    # Iterate over the data unit to get the row data
    rows = []
    for unit_element in unit_elements:
      copy_of_array_atom = self.__get_copy_of_array_atom(self.value,unit_element)
      # replace the atom's select to current unit's web_element
      handler = Array(self.browser,copy_of_array_atom)
      outcome = handler.handle()
      if outcome and outcome.data:
        rows.append(outcome.data)

    return STDOut(data=rows)


  def __get_copy_of_array_atom(self,array_atom,unit_element):
    '''
    Add the unit container' selector as the reader atom's parent selector
    '''
    copy_of_array_atom = copy.deepcopy(array_atom)
    for atom in copy_of_array_atom.get_value():
      # set a selector firstly
      if atom.get_selector():
        atom.set_parent_selector(unit_element)
      else:
        atom.set_selector(unit_element)

    return copy_of_array_atom

