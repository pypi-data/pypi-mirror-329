from .BluesChromeDriver import BluesChromeDriver    

class BluesChromeHeadlessDriver(BluesChromeDriver):
  
  def set_arguments(self):
    arguments = set([
      '--headless'
    ])
    self.arguments = self.arguments.union(arguments)
  
  def set_experimental_options(self):
    # no more options to add
    self.experimental_options.update(dict())