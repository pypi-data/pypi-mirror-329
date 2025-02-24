import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.releaser.VideoReleaserSchema import VideoReleaserSchema

class ChannelsVideoSchema(VideoReleaserSchema):

  PLATFORM = 'channels'

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('Video page','https://channels.weixin.qq.com/platform/post/create')

  def create_fill_atom(self):
    # just get the first value option
    default_option = '.activity-filter-wrap .option-item:nth-of-type(2)'
    #selector_template = '.activity-filter-wrap .option-item[title=${material_title}]'
    atoms = [
      # popup the input
      self.atom_factory.createClickable('show activity dialog','.activity-display-wrap',timeout=10),
      self.atom_factory.createPause('pause',2),
      # type the author
      self.atom_factory.createInput('activity title','.activity-filter-wrap input','${material_title}'),
      self.atom_factory.createPause('pause',4),
      # select the first matched option
      self.atom_factory.createClickable('select a activity',default_option),
      self.atom_factory.createFile('video','.ant-upload input','${material_video}'),
    ]

    self.fill_atom = self.atom_factory.createArray('fields',atoms)

  def create_preview_atom(self):
    return None

  def create_submit_atom(self):
    atoms = [
      self.atom_factory.createClickable('submit','.form-btns .weui-desktop-btn_primary'),
    ]
    self.submit_atom = self.atom_factory.createArray('submit',atoms)

  def create_popup_atom(self):
    return None

  def create_activity_atom(self):
    unit_selector = '.activity-filter-wrap .option-item'
    field_atoms = [
      self.atom_factory.createText('title','.activity-item-info'),
    ]
    array_atom = self.atom_factory.createArray('fields',field_atoms) 
    brief_atom = self.atom_factory.createBrief('briefs',unit_selector,array_atom) 

    switch_atoms = [
      self.atom_factory.createClickable('show activity dialog','.activity-display-wrap',timeout=10),
      self.atom_factory.createPause('pause',2),
      self.atom_factory.createInput('activity title','.activity-filter-wrap input','${material_title}'),
      # wait the otpions stable
      self.atom_factory.createPause('pause',4),
    ]
    switch_atom = self.atom_factory.createArray('switch',switch_atoms) 
    atom_map = {
      'switch':switch_atom,
      'brief':brief_atom,
    }

    self.activity_atom = self.atom_factory.createData('activity map',atom_map)
