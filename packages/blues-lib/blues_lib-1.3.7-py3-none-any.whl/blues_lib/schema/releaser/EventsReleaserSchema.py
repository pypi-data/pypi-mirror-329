from abc import ABC,abstractmethod
from .ReleaserSchema import ReleaserSchema

class EventsReleaserSchema(ReleaserSchema,ABC):

  CHANNEL = 'events'

  def __init__(self):
    # { ArrayAtom } the form controller atom list
    self.content_atom = None
    # { ArrayAtom } 
    self.gallery_atom = None
    # { ArrayAtom }
    self.others_atom = None
    
    super().__init__()

  # override
  def create_sub_fields(self):
    self.create_content_atom()
    self.create_gallery_atom()
    self.create_others_atom()

  @abstractmethod
  def create_content_atom(self):
    pass

  @abstractmethod
  def create_gallery_atom(self):
    pass

  @abstractmethod
  def create_others_atom(self):
    pass

  def create_limit_atom(self):
    limit = {
      'content_max_length':1000,
      'image_max_length':9
    }
    self.limit_atom = self.atom_factory.createData('limit',limit)
