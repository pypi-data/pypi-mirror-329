from abc import ABC,abstractmethod
class AISchemaFactory(ABC):

  @abstractmethod
  def create_qa(self,question):
    pass

