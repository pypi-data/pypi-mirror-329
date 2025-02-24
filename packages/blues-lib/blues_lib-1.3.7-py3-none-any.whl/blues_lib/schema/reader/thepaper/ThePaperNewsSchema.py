import sys,re,os
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))

from schema.reader.NewsReaderSchema import NewsReaderSchema

class ThePaperNewsSchema(NewsReaderSchema,ABC):

  def __init__(self,channel='intl'):
    # news' channel 
    self.channel = channel
    
    super().__init__()
  
  def create_url_atom(self):
    if self.channel == 'intl':
      url = 'https://www.thepaper.cn/channel_122908'

    self.url_atom = self.atom_factory.createURL('ifeng homepage',url)

  def create_brief_atom(self):
    unit_selector = '.ant-row .ant-card-body'
    field_atoms = [
      self.atom_factory.createText('material_title','h2'),
      self.atom_factory.createAttr('material_thumbnail','img','src'),
      # relatvie url /newsDetail_forward_29261369
      self.atom_factory.createAttr('material_url','a','href'), 
    ]
    array_atom = self.atom_factory.createArray('fields',field_atoms,pause=0) 
    self.brief_atom = self.atom_factory.createBrief('briefs',unit_selector,array_atom) 

  def create_material_atom(self):
    '''
    All news material has the same atom strcture
    '''
    # para atom
    para_unit_selector = 'div[class^=index_cententWrap] p,div[class^=index_cententWrap] img'
    para_field_atoms = [
      # use the para selector
      self.atom_factory.createText('text',''),
      self.atom_factory.createAttr('image','','src'),
    ]
    para_array_atom = self.atom_factory.createArray('para fields',para_field_atoms,pause=0) 
    para_atom = self.atom_factory.createPara('material_body',para_unit_selector,para_array_atom) 
    
    # outer atom
    container_selector = 'div[class^=index_leftcontent]'
    field_atoms = [
      self.atom_factory.createText('material_title','h1'),
      self.atom_factory.createText('material_post_date','div[class^=index_headerContent] .ant-space-item:first-child span'),
      para_atom,
    ]
    array_atom = self.atom_factory.createArray('fields',field_atoms,pause=0) 
    self.material_atom = self.atom_factory.createNews('news',container_selector,array_atom) 

  def create_author_atom(self):
    self.author_atom = self.atom_factory.createData('author list',['澎湃'])

