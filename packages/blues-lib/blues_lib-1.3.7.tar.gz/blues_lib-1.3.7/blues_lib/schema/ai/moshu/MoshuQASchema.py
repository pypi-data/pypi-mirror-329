import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.AIQASchema import AIQASchema

class MoshuQASchema(AIQASchema):

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('QA page url','https://open.ai-moshu.cc/')

  def create_question_atom(self):
    atoms = [
      # value placeholder 2: material_body_text
      self.atom_factory.createInput('input','textarea[name=inputVal]','question'),
    ]

    self.question_atom = self.atom_factory.createArray('question',atoms)

  def create_submit_atom(self):
    atoms = [
      # value placeholder 2: material_body_text
      self.atom_factory.createClickable('submit','.search_btn'),
    ]

    self.submit_atom = self.atom_factory.createArray('submit',atoms)

  def create_answer_atom(self):
    para_unit_selector = '.default_title_markdown'
    para_field_atoms = [
      # use the para selector
      self.atom_factory.createText('text',''),
    ]
    para_array_atom = self.atom_factory.createArray('para fields',para_field_atoms) 
    self.answer_atom = self.atom_factory.createPara('answer',para_unit_selector,para_array_atom) 

