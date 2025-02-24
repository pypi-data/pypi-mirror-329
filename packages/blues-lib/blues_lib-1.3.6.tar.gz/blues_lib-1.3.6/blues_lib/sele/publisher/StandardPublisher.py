import sys,os,re,time
from .Publisher import Publisher
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.cleanup.CleanupChain import CleanupChain     

class StandardPublisher(Publisher):
  
  def test(self):
    self.open()

  def accept(self,visitor):
    '''
    Double dispatch with visitor
    Parameters:
      visitor { Visitor }
    '''
    visitor.visit_standard(self)

  def cleanup(self,model):
    schema = model['schema']
    material = model['material']
    request = {
      'browser':self.browser,
      'material':material,
      'log':{
        'pub_platform':schema.PLATFORM,
        'pub_channel':schema.CHANNEL,
      },
      'validity_days':30,
    }
    chain = CleanupChain()
    chain.handle(request)
    


