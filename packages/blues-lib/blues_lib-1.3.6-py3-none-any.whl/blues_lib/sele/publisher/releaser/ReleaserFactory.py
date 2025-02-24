from .EventsReleaser import EventsReleaser
from .NewsReleaser import NewsReleaser

class ReleaserFactory():

  def create(self,browser,schema):
    channel = schema.CHANNEL
    if channel == 'events':
      return self.create_events(browser,schema)
    elif channel == 'news':
      return self.create_news(browser,schema)
    else:
      return None

  def create_events(self,browser,schema):
    return EventsReleaser(browser,schema)

  def create_news(self,browser,schema):
    return NewsReleaser(browser,schema)


