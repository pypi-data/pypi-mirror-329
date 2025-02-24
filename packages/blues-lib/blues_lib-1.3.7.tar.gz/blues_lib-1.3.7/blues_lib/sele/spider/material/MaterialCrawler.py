import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.crawler.CrawlerHandler import CrawlerHandler
from sele.spider.deco.MaterialDeco import MaterialDeco
from sele.behavior.BehaviorChain import BehaviorChain
from pool.BluesMaterialIO import BluesMaterialIO  
from util.BluesConsole import BluesConsole 

class MaterialCrawler(CrawlerHandler):
  '''
  Replace the schema's placeholder by data
  '''
  kind = 'handler'
  
  @MaterialDeco()
  def resolve(self,request):
    '''
    Get one material by one brief
    Parameter:
      request {dict} : schema,count,brief,material
    '''
    if not request or not request.get('schema') or not request.get('browser') or not request.get('brief'):
      return

    if not request.get('schema').material_atom:
      # just assign breif to material
      request['material'] = request.get('brief')
    else:
      request['material'] = self.__crawl(request)
  
  def __crawl(self,request):
    browser = request.get('browser')
    brief = request.get('brief')
    schema = request.get('schema')
    material_atom = schema.material_atom
    url = BluesMaterialIO.get_material_url(brief)

    try:
      browser.open(url)
      handler = BehaviorChain(browser,material_atom)
      # STDOut
      outcome = handler.handle()
      material = outcome.data
      if BluesMaterialIO.is_legal_detail(material):
        return {**brief,**material}
      else:
        self.__sign_unavail(brief,outcome.message)
        return None
    except Exception as e:
      self.__sign_unavail(brief,e)
      return None

  def __sign_unavail(self,brief,message):
    '''
    Sign the unavail material to db, avoid to retry next time
    '''
    title = brief.get('material_title')
    BluesConsole.error('Fail to crawl %s : %s' % (title,message))
    
    entity = {**brief}
    entity['material_status'] = 'illegal'
    result = BluesMaterialIO.insert(entity)
    if result['code'] == 200:
      BluesConsole.info('Signed unavail successfully : %s' % title)
    else:
      BluesConsole.error('Signed unavail failure : %s' % title)

    return result['count']
