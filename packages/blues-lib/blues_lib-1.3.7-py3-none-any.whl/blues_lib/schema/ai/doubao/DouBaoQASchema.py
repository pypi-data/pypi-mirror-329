import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.AIQASchema import AIQASchema

class DouBaoQASchema(AIQASchema):

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('QA page url','https://www.doubao.com/chat/')

  def create_question_atom(self):
    atoms = [
      # value placeholder 2: material_body_text
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
    vertical_copy_sel = 'div[data-testid="receive_message"] button[data-testid="message_action_copy"]'
    horizontal_copy_sel = 'div[data-testid="container_inner_copy_btn"]'
    # horizontal 选择器优先
    copy_sel = [horizontal_copy_sel,vertical_copy_sel]
    self.answer_atom = self.atom_factory.createClickable('copy',copy_sel) 
    
  def create_answer_atom2(self):
    '''
    在问题中必须能明确识别为文章，才会以左右布局的结构返回
    第一行就是标题，标题有几种变体，有时在结构上与普通段落相同
    '''
    container_selector = ''
    # 左右布局格式 , 上下布局普通格式
    left_right_layout_unit_sel = '.zone-container .ace-line'
    top_down_layout_unit_sel = '.flow-markdown-body>div , .flow-markdown-body>h1 , .flow-markdown-body>h2 , .flow-markdown-body>h3 , .flow-markdown-body>h4 , .flow-markdown-body>h5'
    para_unit_selector = left_right_layout_unit_sel+' , '+top_down_layout_unit_sel
    para_field_atoms = [
      self.atom_factory.createText('text',''),
    ]
    para_array_atom = self.atom_factory.createArray('para fields',para_field_atoms,pause=0) 
    para_atom = self.atom_factory.createPara('content',para_unit_selector,para_array_atom) 

    field_atoms = [
      para_atom
    ]
    array_atom = self.atom_factory.createArray('fields',field_atoms,pause=0) 
    self.answer_atom = self.atom_factory.createNews('news',container_selector,array_atom) 

