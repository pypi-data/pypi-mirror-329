from .IFengNewsSchema import IFengNewsSchema

class IFengTechOutpostSchema(IFengNewsSchema):
  
  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('ifeng homepage','https://www.ifeng.com/')

  def create_brief_atom(self):
    unit_selector = '.index_center_box_vOlLP div:not(.index_news_list_DXAWc) p[class^=index_news_list_p]'
    field_atoms = [
      self.atom_factory.createAttr('material_title','a','title'),
      self.atom_factory.createAttr('material_url','a','href'), # get from the unit element
    ]
    array_atom = self.atom_factory.createArray('fields',field_atoms,pause=0) 
    self.brief_atom = self.atom_factory.createBrief('briefs',unit_selector,array_atom) 

