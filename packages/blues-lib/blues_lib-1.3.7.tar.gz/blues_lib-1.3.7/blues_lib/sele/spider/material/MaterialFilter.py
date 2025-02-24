import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.deco.MaterialDeco import MaterialDeco
from sele.spider.crawler.CrawlerHandler import CrawlerHandler
from pool.BluesMaterialIO import BluesMaterialIO  
from util.BluesConsole import BluesConsole    

class MaterialFilter(CrawlerHandler):
  '''
  Remove the unavailable breifs
  '''
  kind = 'handler'

  @MaterialDeco()
  def resolve(self,request):
    if not request or not request.get('material'):
      return
    
    self.__filter(request)

  def __filter(self,request):
    material = request.get('material')
    if not BluesMaterialIO.is_legal_material(material):
      BluesConsole.error('Illegal material of fields')
      request['material'] = None
    elif not self.__is_limit_valid(request):
      BluesConsole.error('Illegal material of text length')
      request['material'] = None

  def __is_limit_valid(self,request):
    schema = request.get('schema')
    material = request.get('material')

    limit = schema.limit_atom.get_value()
    min_len = limit.get('content_min_length',0)

    text_len = len(material.get('material_body_text',''))

    if min_len > text_len:
      return False
    else:
      return True


