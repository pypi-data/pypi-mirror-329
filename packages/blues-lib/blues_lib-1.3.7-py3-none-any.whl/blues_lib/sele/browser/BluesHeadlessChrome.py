from .BluesBrowser import BluesBrowser
from .driver.BluesChromeHeadlessDriver import BluesChromeHeadlessDriver  

class BluesHeadlessChrome(BluesBrowser):

  def __init__(self):
    '''
    @description : Must invoke the super method after the driver has assigned
    '''
    self.driver = BluesChromeHeadlessDriver().get()
    super().__init__()