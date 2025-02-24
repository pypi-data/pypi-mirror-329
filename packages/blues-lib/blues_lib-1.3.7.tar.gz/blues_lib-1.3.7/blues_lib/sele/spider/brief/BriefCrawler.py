import sys,os,re,time
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.crawler.CrawlerHandler import CrawlerHandler
from sele.spider.deco.BriefDeco import BriefDeco
from sele.behavior.BehaviorChain import BehaviorChain
from pool.BluesMaterialIO import BluesMaterialIO  
from util.BluesConsole import BluesConsole 

class BriefCrawler(CrawlerHandler):
  '''
  Replace the schema's placeholder by data
  '''
  kind = 'handler'
  
  @BriefDeco()
  def resolve(self,request):
    '''
    Parameter:
      request {dict} : schema,count,briefs,materials
    '''
    if not request or not request.get('schema') or not request.get('browser'):
      return

    if not request.get('schema').brief_atom:
      return

    briefs = self.__crawl(request)
    self.__console(briefs)
    request['briefs'] = briefs
  
  def __before_crawl(self,browser,before_brief_atom):
    if before_brief_atom:
      handler = BehaviorChain(browser,before_brief_atom)
      handler.handle()
  
  def __crawl(self,request):
    browser = request.get('browser')
    schema = request.get('schema')
    url = schema.url_atom.get_value()
    before_brief_atom = schema.before_brief_atom
    brief_atom = schema.brief_atom

    browser.open(url)
    self.__before_crawl(browser,before_brief_atom)

    handler = BehaviorChain(browser,brief_atom)
    outcome = handler.handle()
    return outcome.data

  def __console(self,briefs):
    if not briefs:
      BluesConsole.error('No available briefs')
    else:
      count = str(len(briefs))
      BluesConsole.success('%s initial briefs were obtained' % count)
