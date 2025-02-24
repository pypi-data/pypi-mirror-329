import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.BluesMaterialIO import BluesMaterialIO
from pool.MaterialLogIO import MaterialLogIO
#from sele.CleanupHandler.deco.SchemaCleanupHandlerDeco import SchemaCleanupHandlerDeco
from sele.cleanup.CleanupHandler import CleanupHandler
from util.BluesURL import BluesURL
from util.BluesDateTime import BluesDateTime
from util.BluesConsole import BluesConsole

class LogUpdater(CleanupHandler):
  '''
  Set the publisher log
  '''
  kind = 'handler'

  #@SchemaCleanupHandlerDeco()
  def resolve(self,request):
    '''
    Parameter:
      request {dict} : 
        - browser {Browser}
        - material {Material}
        - log {dict}
          - pub_platform {str} : the publish platform
          - pub_channel {str} : the publish channel
    '''
    if not request:
      return None
    
    self.__update(request)
  
  def __update(self,request):
    pub_screenshot = self.__screenshot(request)
    material = request.get('material')
    log = request.get('log')
    # add screenshot to log entity
    log['pub_screenshot'] = pub_screenshot
    material_title = material['material_title']

    entity = self.__get_entity(request)
    response = MaterialLogIO.insert(entity)
    self.__console(response,material_title,pub_screenshot)

  def __console(self,response,material_title,shot_path):
    code = response.get('code') 
    message = response.get('message') 
    if code == 200:
      BluesConsole.success('Success to insert log of material [%s], screenshot: [%s]' % (material_title,shot_path))
    else:
      BluesConsole.error('Fail to insert log of material [%s], error: %s' % (material_title,message))

  def __get_entity(self,request):
    material = request.get('material')
    log = request.get('log')
    entity = {
      'pub_m_id':material['material_id'],
      'pub_m_title':material['material_title'],
      'pub_date':BluesDateTime.get_now(),
      'pub_status':material['material_status'],
      'pub_platform':log.get('pub_platform'),
      'pub_channel':log.get('pub_channel'),
      'pub_screenshot':log.get('pub_screenshot')
    }
    return entity
  
  def __screenshot(self,request):
    '''
    Record the submission log
    If submit failure, make a screenshot
    '''
    material = request.get('material')
    browser = request.get('browser')
    dirs = [material['material_site']]
    file_name = '%s_%s.png' % (material['material_status'],material['material_id'])
    shot_dir = BluesMaterialIO.get_screenshot_dir(dirs)
    file_path = BluesURL.get_file_path(shot_dir,file_name)
    return browser.interactor.window.screenshot(file_path)


