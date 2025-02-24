import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.releaser.EventsReleaserSchema import EventsReleaserSchema

class TouTiaoEventsSchema(EventsReleaserSchema):

  PLATFORM = 'events'

