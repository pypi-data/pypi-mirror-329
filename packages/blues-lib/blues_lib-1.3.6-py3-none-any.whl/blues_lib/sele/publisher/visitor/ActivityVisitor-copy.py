import sys,os,re,time
from .Visitor import Visitor
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.behavior.BehaviorChain import BehaviorChain
from sele.transformer.schema.SchemaSelectorReplacer import SchemaSelectorReplacer
from schema.releaser.channels.ChannelsSchemaFactory import ChannelsSchemaFactory
from util.BluesDateTime import BluesDateTime
from util.BluesConsole import BluesConsole

class ActivityVisitor(Visitor):
  '''
  Publish one material several times by select a different activity
  The form has a selection or checkbox field
  '''
  MAX_RECURSIVE_TIME = 24

  def __init__(self,maximum=50,starting_index=0,recursive_interval=-1,recursive_time=0):
    super().__init__()

    # { int } the start option index , sometime the first option is the placehoder, start from 0
    self.starting_index = starting_index
    # { int } the max activity count
    self.maximum = maximum
    # { int } recursive wait time : seconds
    self.recursive_interval = recursive_interval
    # { int } recusize times, current max 24
    self.recursive_time = recursive_time

  def visit_standard(self,publisher) -> None:
    self.publisher = publisher
    self.publish()

  def visit_once_login(self,publisher) -> None:
    self.publisher = publisher
    self.publish()

  def visit_test(self,publisher,callback) -> None:
    self.publisher = publisher
    rows = []
    for i in range(self.maximum):
      self.set_activity_atom(i+1)
      callback(self.publisher.schema)

  # concreate calculate
  def publish(self):
    if not self.publisher.material:
      BluesConsole.error('No available materials')
      return False

    self.publisher.login()
    
    # first time release
    self.multi_release()

    # recursive release
    self.recursive_release()

    self.publisher.quit()

  def recursive_release(self):
    # at leaset wait 60 seconds
    if self.recursive_interval>60 and self.recursive_time>0:
      times = self.recursive_time-1 if self.recursive_time<=self.MAX_RECURSIVE_TIME else self.MAX_RECURSIVE_TIME-1
      for i in range(times):
        BluesConsole.info('Recursive release %s/%s' % ((i+1),(times+1)),'Step')
        BluesConsole.info('Wait %s seconds for next recursive' % self.recursive_interval,'Step')
        time.sleep(self.recursive_interval)
        self.multi_release()

  def multi_release(self):
    # support multi materials
    if self.publisher.schema.materials:
      factory = ChannelsSchemaFactory()
      count = len(self.publisher.schema.materials)
      for i in range(count):
        schema = factory.create_video(i)
        self.publisher.set_schema(schema)
        BluesConsole.info('Video release %s/%s' % ((i+1),count),'SubStep')
        self.release()
    else:
      self.release()
  
  def release(self):
    options = self.get_activity_options()
    if not options or len(options)<self.starting_index+1:
      BluesConsole.error('No activity options')
      return 

    BluesConsole.info('There are currently %s activities: %s' % (len(options),options))
    
    range_value = len(options) - self.starting_index
    for i in range(range_value):
      nth = i+1+self.starting_index
      BluesConsole.info('release %s/%s activity: %s' % (nth,len(options),options[i]))

      # replace the activity element selector dynamically
      self.set_activity_atom(nth)

      # releae the material
      self.publisher.release()

      if nth>=self.maximum+self.starting_index:
        BluesConsole.info('Reach the maximum: %s' % self.maximum)
        break

      time.sleep(15)

  def get_activity_options(self):
    # { ValueAtom } : the value is a dict {'switch': Atom, 'brief': Atom}
    if not self.publisher.schema.activity_atom:
      return None
    
    activity_atom_dict = self.publisher.schema.activity_atom.get_value()
    if not activity_atom_dict:
      return None

    self.publisher.browser.open(self.publisher.url) 

    switch_atom = activity_atom_dict.get('switch')
    brief_atom = activity_atom_dict.get('brief')

    if switch_atom:
      # switch to show the activity selection
      handler = BehaviorChain(self.publisher.browser,switch_atom)
      handler.handle()
      # wait the options render
      BluesDateTime.count_down({'duration':3,'title':'Wait for the activity options to render'})

    handler = BehaviorChain(self.publisher.browser,brief_atom)
    outcome = handler.handle()
    if outcome.data:
      return outcome.data
    else:
      return None
    
  def set_activity_atom(self,nth):
    '''
    Set the activity option
    Parameter:
      nth {int} : the option's index, start from 1 xx:nth-of-type(nth)
    '''
    request = {
      'atom': self.publisher.schema.fill_atom,
      'value':{
        'activity_nth':nth
      }
    }
    handler = SchemaSelectorReplacer()
    handler.handle(request)

