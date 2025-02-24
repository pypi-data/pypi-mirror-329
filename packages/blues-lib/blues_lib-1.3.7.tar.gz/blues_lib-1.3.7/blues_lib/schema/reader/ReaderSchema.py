import sys,os,re
from abc import ABC,abstractmethod
sys.path.append(re.sub('test.*','blues_lib',os.path.realpath(__file__)))
from atom.AtomFactory import AtomFactory     

class ReaderSchema(ABC):
  def __init__(self):
    
    # schema type
    self.type_atom = None

    self.title_prefix_atom = None

    # Decalare fields
    self.atom_factory = AtomFactory()

    # { URLAtom } the list page url
    self.url_atom = None

    # { ValueAtom } The number of crawls expected 
    self.size_atom = None

    # { ValueAtom } Maximum number of images crawled
    self.image_size_atom = None

    # { BriefAtom } the brief atom
    self.brief_atom = None

    # { ArrayAtom } the events before fetch brief
    self.before_brief_atom = None

    # { ArticleAtom } the article atom
    self.material_atom = None

    # {ValueAtom of dict}
    self.limit_atom = None

    # { ValueAtom  of list} the author list
    self.author_atom = None

    # create the fields
    self.create()
  
  # final templte method
  def create(self):
    self.create_schema_type()
    self.create_title_prefix()
    self.create_url_atom()
    self.create_size_atom()
    self.create_image_size_atom()
    self.create_before_brief_atom()
    self.create_brief_atom()
    self.create_material_atom()
    self.create_author_atom()
    self.create_limit_atom()

  # === steps method === 
  def create_schema_type(self):
    self.type_atom = self.atom_factory.createData('schema type','reader')

  def create_title_prefix(self):
    self.title_prefix_atom = self.atom_factory.createData('title prefix','')

  @abstractmethod
  def create_url_atom(self):
    pass

  def create_size_atom(self,size=1):
    self.size_atom = self.atom_factory.createData('Material size',size)

  @abstractmethod
  def create_image_size_atom(self):
    pass

  def create_before_brief_atom(self):
    pass

  @abstractmethod
  def create_brief_atom(self):
    pass

  @abstractmethod
  def create_material_atom(self):
    pass
  
  def create_limit_atom(self):
    limit = {
      'content_min_length':0,
    }
    self.limit_atom = self.atom_factory.createData('limit',limit)

  @abstractmethod
  def create_author_atom(self):
    pass
