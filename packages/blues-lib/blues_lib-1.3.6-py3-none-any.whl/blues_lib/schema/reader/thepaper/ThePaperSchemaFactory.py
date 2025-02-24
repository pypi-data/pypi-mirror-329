import sys,re,os
from .ThePaperNewsSchema import ThePaperNewsSchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.reader.ReaderSchemaFactory import ReaderSchemaFactory

class ThePaperSchemaFactory(ReaderSchemaFactory):

  def create_news(self,channel='intl'):
    return ThePaperNewsSchema(channel)

