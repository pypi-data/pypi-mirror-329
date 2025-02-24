import sys,re,os
from .BBCNewsSchema import BBCNewsSchema
from .BBCGallerySchema import BBCGallerySchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.reader.ReaderSchemaFactory import ReaderSchemaFactory

class BBCSchemaFactory(ReaderSchemaFactory):

  def create_news(self):
    return BBCNewsSchema()

  def create_gallery(self):
    return BBCGallerySchema()
