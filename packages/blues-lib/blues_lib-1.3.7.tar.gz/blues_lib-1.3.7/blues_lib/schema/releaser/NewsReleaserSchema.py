from abc import ABC,abstractmethod
from .ReleaserSchema import ReleaserSchema

class NewsReleaserSchema(ReleaserSchema,ABC):

  CHANNEL = 'news'

  def __init__(self):
    # { ArrayAtom } the form controller atom list
    self.title_atom = None
    # { RichTextAtom } 
    self.content_atom = None
    # { RichTextAtom } 
    self.others_atom = None
    
    super().__init__()

  def create_sub_fields(self):
    self.create_title_atom()
    self.create_content_atom()
    self.create_others_atom()

  @abstractmethod
  def create_title_atom(self):
    pass

  @abstractmethod
  def create_content_atom(self):
    pass

  @abstractmethod
  def create_others_atom(self):
    pass

  def create_limit_atom(self):
    limit = {
      'title_max_length':30,
      'content_max_length':3000,
      'image_max_length':9
    }
    self.limit_atom = self.atom_factory.createData('limit',limit)

