import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.crawler.CrawlerHandler import CrawlerHandler
from sele.spider.deco.MaterialDeco import MaterialDeco
from sele.ai.AIRewriter import AIRewriter
from pool.BluesMaterialIO import BluesMaterialIO
from util.BluesURL import BluesURL 

class MaterialAIRewriter(CrawlerHandler):
  '''
  Extend the required fields by existed fields
  '''
  kind = 'handler'

  @MaterialDeco()
  def resolve(self,request):
    if not request or not request.get('material'):
      return
    
    self.__rewrite(request)

  def __rewrite(self,request):
    material = request.get('material')
    body_text = material.get('material_body_text')
    if not body_text:
      return

    rewriter = AIRewriter('doubao')
    result = rewriter.rewrite_by_texts(body_text,500)
    if result:
      # save the original value to the ori field
      material['material_ori_title'] = material['material_title']
      material['material_ori_body_text'] = material['material_body_text']
      # use ai firstly
      material['material_title'] = result['title']
      material['material_body_text'] = result['paras']
    else:
      # keep the columen as the same
      material['material_ori_title'] = ''
      material['material_ori_body_text'] = ''


