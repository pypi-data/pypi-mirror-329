import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.MACLoginerSchema import MACLoginerSchema

class TouTiaoMACLoginerSchema(MACLoginerSchema):
  pass
