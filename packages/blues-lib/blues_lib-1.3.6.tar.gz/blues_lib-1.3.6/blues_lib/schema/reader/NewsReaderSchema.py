from abc import ABC,abstractmethod
from .ReaderSchema import ReaderSchema

class NewsReaderSchema(ReaderSchema,ABC):

  def create_schema_type(self):
    self.type_atom = self.atom_factory.createData('schema type','article')

  def create_image_size_atom(self):
    self.image_size_atom = self.atom_factory.createData('Max image size',9)

  def create_limit_atom(self):
    limit = {
      'content_min_length':300,
    }
    self.limit_atom = self.atom_factory.createData('limit',limit)

