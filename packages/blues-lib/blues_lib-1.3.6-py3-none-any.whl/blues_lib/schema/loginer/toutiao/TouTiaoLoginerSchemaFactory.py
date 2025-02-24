import sys,os,re
from .TouTiaoAccountLoginerSchema import TouTiaoAccountLoginerSchema
from .TouTiaoMACLoginerSchema import TouTiaoMACLoginerSchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.LoginerSchemaFactory import LoginerSchemaFactory

class TouTiaoLoginerSchemaFactory(LoginerSchemaFactory):

  def create_account_schema(self):
    return TouTiaoAccountLoginerSchema()

  def create_mac_schema(self):
    return TouTiaoMACLoginerSchema()
