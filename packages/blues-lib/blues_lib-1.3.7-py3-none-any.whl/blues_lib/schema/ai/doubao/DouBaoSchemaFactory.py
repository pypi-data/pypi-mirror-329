import sys,os,re,json
from .DouBaoQASchema import DouBaoQASchema
from .DouBaoImgGenSchema import DouBaoImgGenSchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.AISchemaFactory import AISchemaFactory

class DouBaoSchemaFactory(AISchemaFactory):

  def create_qa(self):
    return DouBaoQASchema()

  def create_img_gen(self):
    return DouBaoImgGenSchema()
