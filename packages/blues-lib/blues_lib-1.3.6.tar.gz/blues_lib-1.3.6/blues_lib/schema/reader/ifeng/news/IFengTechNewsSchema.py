from .IFengNewsSchema import IFengNewsSchema

class IFengTechNewsSchema(IFengNewsSchema):
  
  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('ifeng tech','https://tech.ifeng.com/')

  def create_brief_atom(self):
    unit_selector = 'div[class^=index_hotEvent] a[class^=index_content]'
    field_atoms = [
      self.atom_factory.createAttr('material_title','.index_text_content_cdolu','title'),
      self.atom_factory.createAttr('material_url','','href'), # get from the unit element
      self.atom_factory.createAttr('material_thumbnail','img','src')
    ]
    array_atom = self.atom_factory.createArray('fields',field_atoms,pause=0) 
    self.brief_atom = self.atom_factory.createBrief('briefs',unit_selector,array_atom) 

