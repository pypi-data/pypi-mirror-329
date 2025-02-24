import sys,os,re,copy
from abc import ABC,abstractmethod
from .Model import Model
sys.path.append(re.sub('test.*','blues_lib',os.path.realpath(__file__)))
from model.decoder.SchemaValueReplacer import SchemaValueReplacer

class AIQAModel(Model):
    
  def _decode_one(self,schema,material):
    request = {
      'schema':schema,
      'material':material,
    }
    SchemaValueReplacer().handle(request)
  
