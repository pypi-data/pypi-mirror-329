import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
#from sele.CleanupHandler.deco.SchemaCleanupHandlerDeco import SchemaCleanupHandlerDeco
from sele.cleanup.CleanupHandler import CleanupHandler
from util.BluesConsole import BluesConsole

class Notifier(CleanupHandler):
  '''
  Clear the dated material (text / image) and log files
  '''
  kind = 'handler'

  #@SchemaCleanupHandlerDeco()
  def resolve(self,request):
    '''
    Parameter:
      request {dict} : 
        - browser {Browser}
        - material {Material}
        - platform {str} : the publish platform
        - channel {str} : the publish channel
        - validity_days {int} : number of days to retain data
    '''
    self.__mail(request)
    return request
  
  def __mail(self,request):
    '''
    Remove the dated material images
    '''
    material = request.get('material')
    material_title = material.get('material_title')
    material_status = material.get('material_status')
    if material_status=='pubfailure':
      BluesConsole.error('Notice: Fail to publish the material [%s]' % material_title)
    else:
      BluesConsole.success('Notice: Success to publish the material [%s]' % material_title)

