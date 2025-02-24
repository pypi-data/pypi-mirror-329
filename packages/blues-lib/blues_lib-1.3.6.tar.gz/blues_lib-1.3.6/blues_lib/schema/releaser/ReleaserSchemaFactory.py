from abc import ABC,abstractmethod
class ReleaserSchemaFactory(ABC):

  def create_events(self):
    pass

  def create_news(self):
    pass

  def create_video(self):
    pass
