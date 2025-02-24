import sys,re,os
from .gallery.DouBaoGallerySchema import DouBaoGallerySchema
from .gallery.DouBaoPortraitGallerySchema import DouBaoPortraitGallerySchema
from .gallery.DouBaoArtGallerySchema import DouBaoArtGallerySchema
from .gallery.DouBaoProductGallerySchema import DouBaoProductGallerySchema
from .gallery.DouBaoSceneGallerySchema import DouBaoSceneGallerySchema
from .gallery.DouBaoCartoonGallerySchema import DouBaoCartoonGallerySchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.reader.ReaderSchemaFactory import ReaderSchemaFactory

class DouBaoSchemaFactory(ReaderSchemaFactory):

  # all categories
  def create_gallery(self):
    return DouBaoGallerySchema()
  
  def create_gallery_list(self):
    return [
      DouBaoPortraitGallerySchema(), # 人像
      DouBaoArtGallerySchema(), # 艺术
      DouBaoProductGallerySchema(), # 产品
      DouBaoSceneGallerySchema(), # 风景
      DouBaoCartoonGallerySchema(), # 动漫
    ]
