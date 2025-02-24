import sys,re,os
from .DouBaoGallerySchema import DouBaoGallerySchema

class DouBaoSceneGallerySchema(DouBaoGallerySchema):
  
  def create_before_brief_atom(self):
    atoms = [
      # 2- 人像摄影 3-艺术 4-国风 5-动漫 7-商品 8-风景
      self.atom_factory.createClickable('to person photos','.carousel-item div[data-value]:nth-of-type(8)'),
      self.atom_factory.createPause('wait the poptos',5),
    ]
    self.before_brief_atom = self.atom_factory.createArray('before brief',atoms) 
