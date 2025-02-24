import sys,os,re
from .MaterialCrawler import MaterialCrawler  
from .MaterialThumbnail import MaterialThumbnail  
from .MaterialParaImage import MaterialParaImage  
from .MaterialParaText import MaterialParaText  
from .MaterialExtender import MaterialExtender  
from .MaterialAIRewriter import MaterialAIRewriter  
from .MaterialFilter import MaterialFilter  

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.crawler.CrawlerHandler import CrawlerHandler
from sele.spider.deco.MaterialDeco import MaterialDeco

class MaterialCrawlerChain(CrawlerHandler):
  '''
  Basic behavior chain, it's a handler too
  '''
  kind = 'chain'

  @MaterialDeco()
  def resolve(self,request):
    '''
    Deal the atom by the event chain
    '''
    if not request or not request.get('schema') or not request.get('browser') or not request.get('brief'):
      return

    handler = self.__get_chain()
    handler.handle(request)

  def __get_chain(self):
    '''
    Converters must be executed sequentially
    '''
    # writer
    crawler = MaterialCrawler()
    thumbnail = MaterialThumbnail()
    para_image = MaterialParaImage()
    para_text = MaterialParaText()
    extender = MaterialExtender()
    rewriter = MaterialAIRewriter()
    filtee = MaterialFilter()

    crawler.set_next(thumbnail) \
      .set_next(para_image) \
      .set_next(para_text) \
      .set_next(extender) \
      .set_next(rewriter) \
      .set_next(filtee)

    return crawler
