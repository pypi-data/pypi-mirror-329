import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.deco.MaterialDeco import MaterialDeco
from sele.spider.crawler.CrawlerHandler import CrawlerHandler
from pool.BluesMaterialIO import BluesMaterialIO

class MaterialParaImage(CrawlerHandler):
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
    paras = material.get('material_body')
    image_count = 0
    first_image = None
    if not paras:
      return
    for para in paras:
      # download and deal image
      if para['type'] == 'image':
        local_image = BluesMaterialIO.get_download_image(material,para['value'])
        if not local_image:
          continue
        para['value'] = local_image
        if not first_image:
          first_image = local_image    

    self.__pad_image(material,first_image)
    self.__pad_thumbnail(material,first_image)

  def __pad_image(self,material,first_image):
    material_thumbnail = material.get('material_thumbnail')
    paras = material.get('material_body')
    if not first_image and material_thumbnail:
      paras.append({'type':'image','value':material_thumbnail})
  
  def __pad_thumbnail(self,material,first_image):
    if not material['material_thumbnail'] and first_image:
      material['material_thumbnail'] = first_image
