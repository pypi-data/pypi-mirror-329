import sys,os,re,json
from .MoshuQASchema import MoshuQASchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.AISchemaFactory import AISchemaFactory

class MoshuSchemaFactory(AISchemaFactory):

  def create_qa(self,question):
    return MoshuQASchema(question)

