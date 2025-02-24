import sys,os,re,json
from .TouTiaoEventsSchema import TouTiaoEventsSchema
from .TouTiaoNewsSchema import TouTiaoNewsSchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from .ReleaserSchemaFactory import ReleaserSchemaFactory

class TouTiaoSchemaFactory(ReleaserSchemaFactory):

  def create_events(self):
    return TouTiaoEventsSchema()

  def create_news(self):
    return TouTiaoNewsSchema()
