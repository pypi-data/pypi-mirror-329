import sys,os,re,time
from .Publisher import Publisher
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesDateTime import BluesDateTime
from util.BluesConsole import BluesConsole

class OnceLoginPublisher(Publisher):

  def test(self):
    self.open()
      
  def accept(self,visitor):
    '''
    Double dispatch with visitor
    '''
    visitor.visit_once_login(self)

  def login(self):
    self.browser = self.loginer.login()
    if not self.browser:
      BluesConsole.error('Login failure')
      raise Exception('Login failure')

  def open(self):
    self.browser.open(self.url)
    BluesConsole.success('Opened form page: %s' % self.browser.interactor.document.get_title())
    BluesDateTime.count_down({
      'duration':7,
      'title':'Wait the form page ready...'
    })

  def fill(self):
    '''
    Rewrite the parent's fill method to wait
    '''
    super().fill()
    BluesDateTime.count_down({
      'duration':5,
      'title':'Wait the video to upload...'
    })
    BluesConsole.success('Opened form page: %s' % self.browser.interactor.document.get_title())


