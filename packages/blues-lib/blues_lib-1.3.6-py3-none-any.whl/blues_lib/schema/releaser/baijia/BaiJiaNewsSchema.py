import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.releaser.NewsReleaserSchema import NewsReleaserSchema

class BaiJiaNewsSchema(NewsReleaserSchema):

  PLATFORM = 'baijia'

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('news page','https://baijiahao.baidu.com/builder/rc/edit?type=news&is_from_cms=1')

  def create_title_atom(self):
    atoms = [
      self.atom_factory.createPause('Wait the page init',10),
      self.atom_factory.createInput('title','#newsTextArea textarea','${material_title}',timeout=10),
    ]
    self.title_atom = self.atom_factory.createArray('title',atoms)

  def create_others_atom(self):
    thumbnail_atom = self.__get_thumbnail_atom()
    atoms = [
      # switch to single cover mode
      self.atom_factory.createRollin('to cover','.edit-cover-container label:nth-of-type(2) input',{'x':0,'y':150}),
      self.atom_factory.createChoice('single cover','.edit-cover-container label:nth-of-type(2) input'),

      # select a thumbnail
      thumbnail_atom,

      # select a category, before remove the popover or can't click
      self.atom_factory.createPopup('tip','.cheetah-popover'),
      self.atom_factory.createRollin('to category','.cheetah-select-selection-search input',{'x':0,'y':150}),
      self.atom_factory.createClickable('input','.cheetah-select-selection-search input'),
      # set a default option, support standard and activity publish
      self.atom_factory.createClickable('category 1','.cheetah-cascader-menus ul li[title=科技]',selector_template='.cheetah-cascader-menus ul li:nth-of-type(${activity_nth})'),
      # scroll the element to clickable
      self.atom_factory.createClickable('category 2','.cheetah-cascader-menu li[title=互联网]'),
    ]

    self.others_atom = self.atom_factory.createArray('fields',atoms)

  def __get_thumbnail_atom(self):
    replace_or_placehoder = '.coverUploaderView .cover span:last-child,.coverUploaderView .container'
    atoms = [
      # show the upload cover element
      self.atom_factory.createRollin('to cover',replace_or_placehoder,{'x':0,'y':150}),
      # open the dialog, has two elements: replace text icon or placehoder bg
      self.atom_factory.createClickable('popup',replace_or_placehoder,timeout=10),
      # switch to the local image
      self.atom_factory.createClickable('switch','.cheetah-tabs-tabpane-active .image',timeout=10),
      # confirm
      self.atom_factory.createClickable('Upload images','#imageModalEditBtn + button'),
    ]

    return self.atom_factory.createArray('thumbnail',atoms)

  def __get_image_atom(self):
    atoms = [
      self.atom_factory.createClickable('popup','.edui-for-insertimage .edui-default',timeout=10),
      # value placeholder 1: material_body_image ,set wait_time as 5
      # the title must be the material key
      self.atom_factory.createFile('images','.cheetah-upload input','material_body_image',5),
      self.atom_factory.createClickable('Upload images','.cheetah-modal-footer button.cheetah-btn-primary'),
    ]
    return self.atom_factory.createArray('images',atoms)

  def __get_text_atom(self):
    atoms = [
      self.atom_factory.createFrame('to frame','#ueditor_0','in',timeout=20),
      # the value must be the material key , must have 2 line break
      self.atom_factory.createTextArea('texts','body','material_body_text',2),
      self.atom_factory.createFrame('to frame','#ueditor_0','out'),
    ]
    return self.atom_factory.createArray('text',atoms)

  def create_content_atom(self):
    '''
    Fill atoms is a ArrayAtom, the array's taom can't be a complex atom (the atom contains array also)
    '''
    atoms = {
      'image_atom':self.__get_image_atom(),
      'text_atom':self.__get_text_atom(),
      'image_value':self.atom_factory.createData('material_body_image','${material_body_image}'),
      'text_value':self.atom_factory.createData('material_body_text','${material_body_text}'),
    }
    self.content_atom = self.atom_factory.createRichText('richtext','no parent sel',atoms)

  def create_preview_atom(self):
    atoms = [
      self.atom_factory.createPause('wait images to upload',5),
    ]
    self.preview_atom = self.atom_factory.createArray('preview',atoms)

  def create_submit_atom(self):
    atoms = [
      self.atom_factory.createClickable('submit','.editor-component-operator .always-blue')
    ]
    self.submit_atom = self.atom_factory.createArray('popup',atoms)

  def create_popup_atom(self):
    atoms = [
      self.atom_factory.createPopup('tip','.once-tip'),
      self.atom_factory.createPopup('tip','.cheetah-popover'),
      # temp popup
      self.atom_factory.createPopup('test tip','.edit-page-news + *'),
    ]
    self.popup_atom = self.atom_factory.createArray('popup',atoms)

  def create_activity_atom(self):
    unit_selector = '.cheetah-cascader-menus ul li'
    field_atoms = [
      self.atom_factory.createAttr('title','','title'),
    ]
    array_atom = self.atom_factory.createArray('fields',field_atoms) 
    brief_atom = self.atom_factory.createBrief('briefs',unit_selector,array_atom) 

    switch_atoms = [
      self.atom_factory.createPopup('tip','.once-tip'),
      self.atom_factory.createClickable('input','.event-category .cheetah-select-selector'),
    ]
    switch_atom = self.atom_factory.createArray('switch',switch_atoms) 
    atom_dict = {
      'switch':switch_atom,
      'brief':brief_atom,
    }

    self.activity_atom = self.atom_factory.createData('activity map',atom_dict)
