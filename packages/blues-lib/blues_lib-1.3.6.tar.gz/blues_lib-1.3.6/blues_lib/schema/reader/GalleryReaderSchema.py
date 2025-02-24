from abc import ABC,abstractmethod
from .ReaderSchema import ReaderSchema

class GalleryReaderSchema(ReaderSchema,ABC):

  def create_schema_type(self):
    self.type_atom = self.atom_factory.createData('schema type','gallery')

  def create_image_size_atom(self):
    self.image_size_atom = self.atom_factory.createData('Max image size',30)

  def create_material_atom(self):
    pass

  def create_author_atom(self):
    pass