from abc import ABC,abstractmethod

class LoginerFactory(ABC):
  def create_once_mac(self):
    pass

  def create_persistent_mac(self):
    pass