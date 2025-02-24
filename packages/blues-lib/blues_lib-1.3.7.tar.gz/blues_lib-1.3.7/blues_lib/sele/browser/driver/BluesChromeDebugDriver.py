from .BluesChromeDriver import BluesChromeDriver    

class BluesChromeDebugDriver(BluesChromeDriver):
  

  def __init__(self,debugger_addr='localhost:8888'):
    super().__init__()
    self.__debugger_addr = debugger_addr

  def set_arguments(self):
    # no more arguments to add
    self.arguments = self.arguments.union(set())
  
  def set_experimental_options(self):
    '''
    @description : cover all options, can't use those default experimental options in debug mode,
      because the chrome had been opened
    '''
    options = {
      'debuggerAddress':self.__debugger_addr
    }
    self.experimental_options = options
  