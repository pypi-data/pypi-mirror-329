from .BluesBrowser import BluesBrowser
from .driver.BluesChromeStandardDriver import BluesChromeStandardDriver  

class BluesStandardChrome(BluesBrowser):

  def __init__(self):
    '''
    @description : Must invoke the super method after the driver has assigned
    '''
    self.driver = BluesChromeStandardDriver().get()
    super().__init__()