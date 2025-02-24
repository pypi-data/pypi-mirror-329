from seleniumwire import webdriver
from .BluesChromeDriver import BluesChromeDriver    

# https://pypi.org/project/selenium-wire/
class BluesChromeProxyDriver(BluesChromeDriver):
  
  def set_selenium_driver(self):
    # not the selenium's webdriver
    self.selenium_driver = webdriver

  def set_arguments(self):
    # no more arguments to add
    self.arguments = self.arguments.union(set())
  
  def set_experimental_options(self):
    # no more options to add
    self.experimental_options.update(dict())
