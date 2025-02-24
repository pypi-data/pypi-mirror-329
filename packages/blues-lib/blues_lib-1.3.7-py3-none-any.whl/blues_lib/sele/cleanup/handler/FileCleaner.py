import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.BluesMaterialIO import BluesMaterialIO
#from sele.CleanupHandler.deco.SchemaCleanupHandlerDeco import SchemaCleanupHandlerDeco
from sele.cleanup.CleanupHandler import CleanupHandler
from util.BluesFiler import BluesFiler
from util.BluesConsole import BluesConsole

class FileCleaner(CleanupHandler):
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
        - log {dict}
          - platform {str} : the publish platform
          - channel {str} : the publish channel
        - validity_days {int} : number of days to retain data
    '''
    self.__clear_material(request)
    self.__clear_log(request)
    return request
  
  def __clear_material(self,request):
    '''
    Remove the dated material images
    '''
    material_root = BluesMaterialIO.get_material_root()
    validity_days = request.get('validity_days',30)
    count = BluesFiler.removedirs(material_root,validity_days)
    if count:
      BluesConsole.success('Success to remove the dated (more than %s days) [%s] materials from [%s]' % (validity_days,count,material_root))
    else:
      BluesConsole.info('No dated (more than %s days) materials in [%s]' % (validity_days,material_root))

  def __clear_log(self,request):
    '''
    Remove the dated published end screenshot
    '''
    log_root = BluesMaterialIO.get_log_root()
    validity_days = request.get('validity_days',30)
    count = BluesFiler.removedirs(log_root,validity_days)
    if count:
      BluesConsole.success('Success to remove the dated (more than %s days) [%s] log from [%s]' % (validity_days,count,log_root))
    else:
      BluesConsole.info('No dated (more than %s days) log in [%s]' % (validity_days,log_root))

