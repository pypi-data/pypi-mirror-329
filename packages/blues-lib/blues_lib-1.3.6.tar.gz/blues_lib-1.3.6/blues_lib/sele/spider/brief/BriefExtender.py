import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.crawler.CrawlerHandler import CrawlerHandler
from sele.spider.deco.BriefDeco import BriefDeco
from util.BluesURL import BluesURL 
from util.BluesAlgorithm import BluesAlgorithm 

class BriefExtender(CrawlerHandler):
  '''
  Extend the required fields by existed fields
  '''
  kind = 'handler'
  
  @BriefDeco()
  def resolve(self,request):
    if not request or not request.get('briefs'):
      return
    
    self.__extend(request)

  def __extend(self,request):
    briefs = request.get('briefs')
    for brief in briefs:
      self.__extend_site(brief)
      self.__extend_id(brief)
      

  def __extend_site(self,brief):
    url = brief['material_url']
    material_site = BluesURL.get_main_domain(url)
    brief['material_site'] = material_site

  def __extend_id(self,brief):
    url = brief['material_url']
    site = brief['material_site']
    if len(url)>32:
      material_id = site+'_'+BluesAlgorithm.md5(url)
    else:
      material_id = site+'_'+BluesURL.get_file_name(url)
    brief['material_id'] = material_id

