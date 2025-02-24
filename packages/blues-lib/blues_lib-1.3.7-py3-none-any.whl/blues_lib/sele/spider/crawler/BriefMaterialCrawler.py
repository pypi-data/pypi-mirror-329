import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.material.MaterialCrawlerChain import MaterialCrawlerChain  
from sele.spider.deco.BriefMaterialDeco import BriefMaterialDeco
from sele.spider.crawler.CrawlerHandler import CrawlerHandler
from pool.BluesMaterialIO import BluesMaterialIO  
from util.BluesConsole import BluesConsole 

class BriefMaterialCrawler(CrawlerHandler):
  '''
  Linke the brief chain to the material chain
  '''
  kind = 'handler'
  
  @BriefMaterialDeco()
  def resolve(self,request):
    '''
    Parameter:
      request {dict} : the brief hander's request: schema,count,briefs,materials
    '''
    if not request or not request.get('schema') or not request.get('browser') or not request.get('briefs'):
      return

    materials = self.__crawl(request)
    request['materials'] = materials
  
  def __crawl(self,request):
    schema = request.get('schema')
    briefs = request.get('briefs')
    size = schema.size_atom.get_value()

    mateirals = []
    handler = MaterialCrawlerChain()
    for brief in briefs:
      request['brief'] = brief
      handler.handle(request)
      material = request.get('material')
      if material:
        request['material'] = None # remove the materail attr
        mateirals.append(material)
      if len(mateirals) >= size:
        break
    return mateirals

