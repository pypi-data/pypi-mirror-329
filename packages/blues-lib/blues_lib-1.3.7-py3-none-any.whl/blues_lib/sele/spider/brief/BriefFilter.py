import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.crawler.CrawlerHandler import CrawlerHandler
from sele.spider.deco.BriefDeco import BriefDeco
from pool.BluesMaterialIO import BluesMaterialIO  
from util.BluesURL import BluesURL 
from util.BluesConsole import BluesConsole 

class BriefFilter(CrawlerHandler):
  '''
  Remove the unavailable breifs
  '''
  kind = 'handler'
  
  @BriefDeco()
  def resolve(self,request):
    if not request or not request.get('briefs'):
      return
    
    avail_briefs = self.__filter(request)
    request['briefs'] = avail_briefs

  def __filter(self,request):
    briefs = request.get('briefs')
    avail_briefs = [] 
    
    for brief in briefs:

      title = brief['material_title']

      if not self.__is_legal_origin(request,brief):
        BluesConsole.error('Unavial biref [Not Same Origin] : %s' % title)
        continue
      if not BluesMaterialIO.is_legal_brief(brief):
        BluesConsole.error('Unavial biref [Not Legal] : %s' % title)
        continue
      if BluesMaterialIO.exist(brief):
        BluesConsole.error('Unavial biref [Exist] : %s' % title)
        continue

      avail_briefs.append(brief)

    return avail_briefs if avail_briefs else None

  def __is_legal_origin(self,request,brief):
    '''
    The brief's url must be the same to the platform url
    '''
    schema = request.get('schema')
    schema_type = schema.type_atom.get_value()
    # temp pass
    if schema_type == 'gallery' :
      return True

    site_url = schema.url_atom.get_value()
    site_domain = BluesURL.get_main_domain(site_url) 

    material_url = brief['material_url']
    material_domain = BluesURL.get_main_domain(material_url) 

    return site_domain == material_domain
