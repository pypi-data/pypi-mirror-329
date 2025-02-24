import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.deco.MaterialDeco import MaterialDeco
from sele.spider.crawler.CrawlerHandler import CrawlerHandler
from pool.BluesMaterialIO import BluesMaterialIO

class MaterialThumbnail(CrawlerHandler):
  '''
  Extend the required fields by existed fields
  '''
  kind = 'handler'

  @MaterialDeco()
  def resolve(self,request):
    if not request or not request.get('material'):
      return
    
    self.__download(request)

  def __download(self,request):
    material = request.get('material')
    # convert online image to local image
    material['material_thumbnail'] = BluesMaterialIO.get_download_thumbnail(material)
