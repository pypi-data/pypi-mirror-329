import sys,re,os
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.reader.NewsReaderSchema import NewsReaderSchema

class IFengNewsSchema(NewsReaderSchema,ABC):
  
  def create_url_atom(self):
    pass

  def create_brief_atom(self):
    pass

  def create_material_atom(self):
    '''
    All news material has the same atom strcture
    '''
    # para atom
    para_unit_selector = 'div[class^=index_text] p:not(.picIntro)'
    para_field_atoms = [
      # use the para selector
      self.atom_factory.createText('text',''),
      self.atom_factory.createAttr('image','img','data-lazyload'),
    ]
    para_array_atom = self.atom_factory.createArray('para fields',para_field_atoms,pause=0) 
    para_atom = self.atom_factory.createPara('material_body',para_unit_selector,para_array_atom) 
    
    # outer atom
    container_selector = 'div[class^=index_leftContent]'
    field_atoms = [
      self.atom_factory.createText('material_title','h1'),
      self.atom_factory.createText('material_post_date','div[class^=index_timeBref] a'),
      para_atom,
    ]
    array_atom = self.atom_factory.createArray('fields',field_atoms,pause=0) 
    self.material_atom = self.atom_factory.createNews('news',container_selector,array_atom) 

  def create_author_atom(self):
    self.author_atom = self.atom_factory.createData('author list',['凤凰网','凤凰新闻'])

