import sys,os,re
from .ModelFactory import ModelFactory

sys.path.append(re.sub('test.*','blues_lib',os.path.realpath(__file__)))
from model.MaterialModel import MaterialModel
from schema.releaser.baijia.BaiJiaSchemaFactory import BaiJiaSchemaFactory
from material.ChannelDBMaterial import ChannelDBMaterial     

class BaiJiaDBModelFactory(ModelFactory):

  PLATFORM = 'baijia'
  QUERY_CONDITION = {
    'mode':'latest',
    'count':1,
  }

  def __init__(self):
    self.schema_factory = BaiJiaSchemaFactory()

  def create(self,current_quota,query_condition=None):
    condition = query_condition if query_condition else self.QUERY_CONDITION
    return self.__get_channel_models(current_quota,condition)

  def create_events(self,query_condition=None):
    current_quota = {
      'events':self.__get_query_count(query_condition)
    }
    return self.create(current_quota,query_condition)

  def create_news(self,query_condition=None):
    current_quota = {
      'news':self.__get_query_count(query_condition)
    }
    return self.create(current_quota,query_condition)

  def __get_query_count(self,query_condition):
    count = 0
    if query_condition:
      count = query_condition.get('count')
    if not count:
      count = self.QUERY_CONDITION.get('count')
    return count

  def __get_channel_models(self,current_quota,query_condition):
  
    db_material = ChannelDBMaterial(self.PLATFORM,current_quota,query_condition)
    channel_materials = db_material.get()
    
    if not channel_materials:
      return None
    
    models = []
    for channel,materials in channel_materials.items():
      schema = self.__get_channel_schema(channel)
      if not schema:
        continue
      channel_models = MaterialModel(schema,materials).get()
      models += channel_models 

    return (models if models else None)

  def __get_channel_schema(self,channel):
    schema = None
    if channel == 'events':
      schema = self.schema_factory.create_events()
    elif channel == 'news':
      schema = self.schema_factory.create_news()
    return schema

