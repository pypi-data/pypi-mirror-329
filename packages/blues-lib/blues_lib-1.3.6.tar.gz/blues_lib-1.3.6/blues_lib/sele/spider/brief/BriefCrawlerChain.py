import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.crawler.CrawlerHandler import CrawlerHandler
from sele.spider.deco.BriefDeco import BriefDeco
from .BriefCrawler import BriefCrawler  
from .BriefExtender import BriefExtender  
from .BriefFilter import BriefFilter  

class BriefCrawlerChain(CrawlerHandler):
  '''
  Basic behavior chain, it's a handler too
  '''
  kind = 'chain'
  
  @BriefDeco()
  def resolve(self,request):
    '''
    Deal the atom by the event chain
    '''
    handler = self.__get_chain()
    handler.handle(request)

  def __get_chain(self):
    '''
    Converters must be executed sequentially
    '''
    # writer
    brief_crawler = BriefCrawler()
    brief_extender = BriefExtender()
    brief_filter = BriefFilter()
    
    # must inovke the extender before the filter
    brief_crawler.set_next(brief_extender) \
      .set_next(brief_filter)

    return brief_crawler
