import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.deco.MaterialDeco import MaterialDeco
from sele.spider.crawler.CrawlerHandler import CrawlerHandler

class MaterialParaText(CrawlerHandler):
  '''
  Extend the required fields by existed fields
  '''
  kind = 'handler'

  @MaterialDeco()
  def resolve(self,request):
    if not request or not request.get('material'):
      return
    
    self.__replace(request)

  def __replace(self,request):
    material = request.get('material')
    schema = request.get('schema')
    paras = material.get('material_body')
    if not paras:
      return
    original_authors = schema.author_atom.get_value()
    for para in paras:
      # download and deal image
      if para['type'] == 'text': 
        # replace the author
        para['value'] = self.__get_clean_text(para['value'],original_authors)

  def __get_clean_text(self,text,original_authors):
    # replace the author
    system_author = '深蓝'
    if not original_authors:
      return text

    clean_text = text
    for author in original_authors:
      clean_text = clean_text.replace(author,system_author)

    return clean_text
