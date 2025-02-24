import sys,os,re,subprocess,time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from .BluesBrowser import BluesBrowser
from .driver.BluesChromeDebugDriver import BluesChromeDebugDriver   

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesPowerShell import BluesPowerShell 

# debug模式下chrome被PS提前打开，不是由webdriver启动，wire无法实现代理
class BluesDebugChrome(BluesBrowser):
  # cover the parent options.detach and prefs can't be set in debug mode
  __CHROME_EXE = BluesPowerShell.get_env_value('CHROME_EXE')
  __DEFAULTS = {
    '--user-data-dir':'c:/sele/debug',
    '--remote-debugging-host':'localhost',
    '--remote-debugging-port':'8888',
  }
  def __init__(self,debug_config={}):
    # must open the debug chrome before create the driver instance
    self.__config = {**self.__DEFAULTS,**debug_config}
    self.start()
    self.driver = BluesChromeDebugDriver(self.__get_debugger_addr()).get()
    super().__init__()

  def __get_debugger_addr(self):
    return '%s:%s' % (self.__config['--remote-debugging-host'],self.__config['--remote-debugging-port'])
  
  def start(self):
    '''
    @description : repopen the specific chrome (stop all chrome processes)
    '''
    self.stop()
    args = ''
    for key,value in self.__config.items():
      args+= ' %s="%s" ' % (key,value)
    result = BluesPowerShell.start_process(self.__CHROME_EXE,args)
    if result['code']!=200:
      raise Exception('Chrome restart failure %s' % result['message'])
  
  def stop(self):
    '''
    @description : stop the all chrome process
    '''
    BluesPowerShell.stop_process('chrome')

