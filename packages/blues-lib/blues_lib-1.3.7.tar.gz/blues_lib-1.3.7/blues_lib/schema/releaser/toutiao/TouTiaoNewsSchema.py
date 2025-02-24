import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.releaser.NewsReleaserSchema import NewsReleaserSchema

class TouTiaoNewsSchema(NewsReleaserSchema):

  PLATFORM = 'news'

