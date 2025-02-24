import sys,os,re,copy
from abc import ABC,abstractmethod
from .Model import Model
from .decoder.SchemaDecoderChain import SchemaDecoderChain     

class MaterialModel(Model):
    
  def _decode_one(self,schema,material):
    SchemaDecoderChain().handle({
      'schema':schema,
      'material':material,
    })
  
