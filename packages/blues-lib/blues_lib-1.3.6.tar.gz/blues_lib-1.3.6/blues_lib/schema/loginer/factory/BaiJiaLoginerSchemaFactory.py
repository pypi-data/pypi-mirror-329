import sys,os,re

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.factory.LoginerSchemaFactory import LoginerSchemaFactory
from schema.loginer.baijia.BaiJiaAccountLoginerSchema import BaiJiaAccountLoginerSchema
from schema.loginer.baijia.BaiJiaMACLoginerSchema import BaiJiaMACLoginerSchema

class BaiJiaLoginerSchemaFactory(LoginerSchemaFactory):

  def create_account(self):
    return BaiJiaAccountLoginerSchema()

  def create_mac(self):
    return BaiJiaMACLoginerSchema()
