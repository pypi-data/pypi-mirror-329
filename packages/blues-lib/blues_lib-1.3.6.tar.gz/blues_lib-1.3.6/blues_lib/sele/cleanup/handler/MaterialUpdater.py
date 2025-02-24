import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.BluesMaterialIO import BluesMaterialIO
#from sele.CleanupHandler.deco.SchemaCleanupHandlerDeco import SchemaCleanupHandlerDeco
from sele.cleanup.CleanupHandler import CleanupHandler
from util.BluesConsole import BluesConsole

class MaterialUpdater(CleanupHandler):
  '''
  Update the material_status after it was published
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
          - platform {str} : the publish platform
          - channel {str} : the publish channel
    '''
    if not request:
      return None
    
    self.__update(request)
  
  def __update(self,request):
    material = request.get('material')
    material_id = material.get('material_id')
    material_title = material.get('material_title')
    material_status = material.get('material_status')
    entity = {'material_status':material_status}      
    conditions = [
      {'field':'material_id','comparator':'=','value':material_id}
    ]
    response = BluesMaterialIO.update(entity,conditions)
    self.__console(response,material_title,material_status)

  def __console(self,response,material_title,material_status):
    code = response.get('code') 
    count = response.get('count') 
    message = response.get('message') 
    if code == 200:
      if count == 0:
        BluesConsole.info('The status of material [%s] is equal to [%s]' % (material_title,material_status))
      else:
        BluesConsole.success('Success to update the status of material [%s] to [%s]' % (material_title,material_status))
    else:
      BluesConsole.error('Fail to update the status of material [%s], message : %s' % (material_title,message))

