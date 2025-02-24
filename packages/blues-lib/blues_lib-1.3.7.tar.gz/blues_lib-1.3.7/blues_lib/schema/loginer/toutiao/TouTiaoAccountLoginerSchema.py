import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.AccountLoginerSchema import AccountLoginerSchema

class TouTiaoAccountLoginerSchema(AccountLoginerSchema):
  pass
