import sys,re,os
from .news.IFengTechNewsSchema import IFengTechNewsSchema
from .news.IFengHotNewsSchema import IFengHotNewsSchema
from .news.IFengTechOutpostSchema import IFengTechOutpostSchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.reader.ReaderSchemaFactory import ReaderSchemaFactory

class IFengSchemaFactory(ReaderSchemaFactory):

  def create_tech_news(self):
    return IFengTechNewsSchema()

  def create_hot_news(self):
    return IFengHotNewsSchema()

  def create_tech_outpost(self):
    return IFengTechOutpostSchema()

