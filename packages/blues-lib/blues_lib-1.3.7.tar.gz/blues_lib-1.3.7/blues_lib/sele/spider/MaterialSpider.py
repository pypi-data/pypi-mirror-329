import sys,re,os,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.crawler.CrawlerChain  import CrawlerChain  
from sele.browser.BluesStandardChrome import BluesStandardChrome
from pool.BluesMaterialIO import BluesMaterialIO
from util.BluesConsole import BluesConsole 

class MaterialSpider():

  def __init__(self,schemas,total=1,persistent=True):
    '''
    Crawl the total count materials from the schemas
    Parameters:
      schemas {List<Schema>} : multi platform or channels' schema
      total {int} : the total excepted crawled count
      persistent {bool} : weather insert to the db
    '''
    self.schemas = schemas if type(schemas)==list else [schemas]
    self.total = total
    self.persistent = persistent
    self.browser = None

  def spide(self):
    self.browser = BluesStandardChrome()
    count = self.__crawl()
    BluesConsole.success('Crawled All/Total = %s/%s : ' % (count,self.total))
    self.browser.quit()

  def __crawl(self):
    '''
    Quantity allocation strategy:
      style 1: Single platform preferred
      style 2: Average distribution of platform
    '''
    crawled_count = 0
    gap_count = self.total

    for schema in self.schemas:

      # use style 1
      schema.create_size_atom(gap_count)

      count = self.__crawl_once(schema)
      self.__console_platform(schema,count)

      crawled_count += count
      gap_count -= count

      if crawled_count >= self.total:
        break

    return crawled_count

  def __console_platform(self,schema,count):
      url = schema.url_atom.get_value()
      BluesConsole.success('Platform/Total = %s/%s : %s' % (count,self.total,url))

  def __crawl_once(self,schema):
    '''
    Crawl one or multi materials from the same schema
    '''
    request = {
      'browser':self.browser,
      'schema':schema,
      'briefs':None,
      'materials':None,
    }
    handler = CrawlerChain()
    handler.handle(request)

    materials = request.get('materials')
    count = len(materials) if materials else 0
    self.__insert(request)
    self.__console(request,count)
    return count

  def __insert(self,request):
    if not self.persistent:
      return 0

    materials = request.get('materials')
    if not materials:
      return 0

    result = BluesMaterialIO.insert(materials)
    if result['code'] == 200:
      BluesConsole.success('Inserted %s materials successfully' % result['count'])
      return result['count']
    else:
      BluesConsole.error('Failed to insert, %s' % result.get('message'))
      return 0


  def __console(self,request,count):
    schema = request.get('schema')
    url = schema.url_atom.get_value()

    if not count:
      BluesConsole.error('Crawled 0 materials from %s' % url)
    else:
      values = (count,url)
      BluesConsole.success('Crawled %s materials from  %s' % values)
      self.__console_title(request)

  def __console_title(self,request):
    materials = request.get('materials')
    i = 1
    for material in materials:
      values = (i,material.get('material_title'))
      BluesConsole.success('%s. %s' % values)
      i+=1

