import sys,re,os
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.reader.GalleryReaderSchema import GalleryReaderSchema

class DouBaoGallerySchema(GalleryReaderSchema):
  
  def create_title_prefix(self):
    self.title_prefix_atom = self.atom_factory.createData('title prefix','【豆包文生图】')

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('DouBao gallery','https://www.doubao.com/chat/create-image')

  def create_before_brief_atom(self):
    # fetch all categories photoes
    atoms = [
      self.atom_factory.createPause('wait the poptos',5),
    ]
    self.before_brief_atom = self.atom_factory.createArray('before brief',atoms) 


  def create_brief_atom(self):
    unit_selector = 'div[data-testid="waterfall-image-list"] div[data-testid="skill-page-image-template-item"]'
    field_atoms = [
      self.atom_factory.createJSText('material_title','div[data-testid="skill-page-image-template-item-title"]',None),
      self.atom_factory.createAttr('material_url','img','src'),
      self.atom_factory.createAttr('material_thumbnail','img','src'),
    ]
    array_atom = self.atom_factory.createArray('fields',field_atoms,pause=0) 
    self.brief_atom = self.atom_factory.createBrief('briefs',unit_selector,array_atom) 

  def create_image_size_atom(self):
    self.image_size_atom = self.atom_factory.createData('Max image size',5)