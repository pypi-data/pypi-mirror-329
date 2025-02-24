import sys,os,re,json
from .BaiJiaEventsSchema import BaiJiaEventsSchema
from .BaiJiaNewsSchema import BaiJiaNewsSchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.releaser.ReleaserSchemaFactory import ReleaserSchemaFactory

class BaiJiaSchemaFactory(ReleaserSchemaFactory):

  def create_events(self):
    return BaiJiaEventsSchema()

  def create_news(self):
    return BaiJiaNewsSchema()
