import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.releaser.EventsReleaserSchema import EventsReleaserSchema

class BaiJiaEventsSchema(EventsReleaserSchema):
  
  PLATFORM = 'baijia'

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('events page','https://baijiahao.baidu.com/builder/rc/edit?type=events')

  def create_content_atom(self):
    atoms = [
      # value placeholder 2: material_body_text
      self.atom_factory.createTextArea('content','#content','${material_body_text}',1),
    ]
    self.content_atom = self.atom_factory.createArray('content atom',atoms)

  def create_others_atom(self):
    atoms = [
      # select a category, before remove the popover or can't click
      self.atom_factory.createPopup('tip','.cheetah-popover'),
      self.atom_factory.createClickable('input','.event-category .cheetah-select-selector'),
      # set a default option, support standard and activity publish
      self.atom_factory.createClickable('category 1','.cheetah-cascader-menus ul li[title=科技]',selector_template='.cheetah-cascader-menus ul li:nth-of-type(${activity_nth})'),
      # scroll the element to clickable
      self.atom_factory.createClickable('category 2','.cheetah-cascader-menu li[title=互联网]'),

      # activty
      #self.atom_factory.createClickable('activity','.event-task .cheetah-public:nth-of-type(1)'),

      # events to news when length>1000, and scroll the element to clickable
      self.atom_factory.createRollin('events to news','#event2news',{'x':0,'y':150}),
      self.atom_factory.createChoice('events to news','#event2news'),
    ]

    self.others_atom = self.atom_factory.createArray('content atom',atoms)

  def create_gallery_atom(self):
    # use the filed plachehoders
    atoms = [
      self.atom_factory.createClickable('Popup the dialog','.uploader-plus'),
      # value placeholder 1: material_body_image ,set wait_time as 5
      self.atom_factory.createFile('Select images','.cheetah-upload input','${material_body_image}',5),
      self.atom_factory.createClickable('Upload images','.cheetah-modal-footer button.cheetah-btn-primary'),
    ]

    self.gallery_atom = self.atom_factory.createArray('gallery atom',atoms)

  def create_preview_atom(self):
    return None

  def create_submit_atom(self):
    atoms = [
      self.atom_factory.createClickable('submit','.events-op-bar-pub-btn.events-op-bar-pub-btn-blue'),
    ]
    self.submit_atom = self.atom_factory.createArray('submit',atoms)

  def create_popup_atom(self):
    atoms = [
      self.atom_factory.createPopup('tip','.once-tip'),
      self.atom_factory.createPopup('tip','.cheetah-popover'),
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
