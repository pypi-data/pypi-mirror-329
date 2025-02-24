import sys,os,re
from .MoshuAccountSchema import MoshuAccountSchema
from .MoshuMACLoginerSchema import MoshuMACLoginerSchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.LoginerSchemaFactory import LoginerSchemaFactory

class MoshuLoginerSchemaFactory(LoginerSchemaFactory):

  def create_account(self):
    return MoshuAccountSchema()

