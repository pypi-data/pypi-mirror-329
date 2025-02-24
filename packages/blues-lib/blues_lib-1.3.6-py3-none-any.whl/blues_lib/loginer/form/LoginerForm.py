from abc import ABC,abstractmethod

class LoginerForm(ABC):
  def __init__(self,schema):
    # { LoginerSchema } 
    self.schema = schema
    # { BluesChrome }
    self.browser = None