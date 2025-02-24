import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.AIQASchema import AIQASchema

class DouBaoImgGenSchema(AIQASchema):

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('QA page url','https://www.doubao.com/chat')
  
  def create_size_atom(self):
    # max fetched image count
    self.size_atom = self.atom_factory.createData('Max size',10)

  def create_question_atom(self):
    atoms = [
      # Toggle to image generation channel
      #self.atom_factory.createClickable('swich','div[data-testid="create_conversation_button"]'),
      self.atom_factory.createInput('input','textarea.semi-input-textarea','${question}'),
    ]

    self.question_atom = self.atom_factory.createArray('question',atoms)

  def create_submit_atom(self):
    atoms = [
      # value placeholder 2: material_body_text
      self.atom_factory.createClickable('submit','#flow-end-msg-send'),
    ]

    self.submit_atom = self.atom_factory.createArray('submit',atoms)

  def create_answer_atom(self):
    unit_selector = 'picture'
    field_atoms = [
      self.atom_factory.createAttr('material_thumbnail','img','src'),
    ]
    array_atom = self.atom_factory.createArray('fields',field_atoms,pause=0) 
    self.answer_atom = self.atom_factory.createBrief('briefs',unit_selector,array_atom) 
