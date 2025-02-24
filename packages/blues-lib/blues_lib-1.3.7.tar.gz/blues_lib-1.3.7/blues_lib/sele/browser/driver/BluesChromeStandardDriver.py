from .BluesChromeDriver import BluesChromeDriver    

class BluesChromeStandardDriver(BluesChromeDriver):
  
  def set_arguments(self):
    # no more arguments to add
    self.arguments = self.arguments.union(set())
  
  def set_experimental_options(self):
    # no more options to add
    self.experimental_options.update(dict())