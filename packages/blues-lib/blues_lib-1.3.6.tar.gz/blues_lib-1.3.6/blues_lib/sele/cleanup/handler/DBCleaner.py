import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.BluesMaterialIO import BluesMaterialIO
from pool.MaterialLogIO import MaterialLogIO
from pool.DBTableIO import DBTableIO
#from sele.CleanupHandler.deco.SchemaCleanupHandlerDeco import SchemaCleanupHandlerDeco
from sele.cleanup.CleanupHandler import CleanupHandler
from util.BluesConsole import BluesConsole

class DBCleaner(CleanupHandler):
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
        - log {dict}
          - channel {str} : the publish channel
          - validity_days {int} : number of days to retain data
    '''
    self.__clear_material(request)
    self.__clear_log(request)
    self.__clear_loginer(request)
    return request
  
  def __clear_material(self,request):
    '''
    Clear the dated meteiral and log rows
    '''
    validity_days = request.get('validity_days',30)
    conditions = [
      {
        'field':'material_collect_date',
        'comparator':'<=',
        'value':'DATE_SUB(CURRENT_DATE, INTERVAL %s DAY)' % validity_days,
        'value_type':'function',
      }
    ]
    response = BluesMaterialIO.delete(conditions)
    self.__console(response,validity_days,'materials')

  def __clear_log(self,request):
    '''
    Clear the dated meteiral and log rows
    '''
    validity_days = request.get('validity_days',30)
    conditions = [
      {
        'field':'pub_date',
        'comparator':'<=',
        'value':'DATE_SUB(CURRENT_DATE, INTERVAL %s DAY)' % validity_days,
        'value_type':'function',
      }
    ]
    response = MaterialLogIO.delete(conditions)
    self.__console(response,validity_days,'log')

  def __clear_loginer(self,request):
    '''
    Clear the dated meteiral and log rows
    '''
    validity_days = request.get('validity_days',30)
    conditions = [
      {
        'field':'login_created_time',
        'comparator':'<=',
        'value':'DATE_SUB(CURRENT_DATE, INTERVAL %s DAY)' % validity_days,
        'value_type':'function',
      }
    ]
    response = DBTableIO('naps_loginer').delete(conditions)
    self.__console(response,validity_days,'loginer')

  def __console(self,response,validity_days,title):
    code = response.get('code') 
    count = response.get('count') 
    message = response.get('message') 
    if code == 200:
      if count == 0:
        BluesConsole.info('No dated (more than %s days) %s in DB' % (validity_days,title))
      else:
        BluesConsole.success('Success to remove the dated (more than %s days) [%s] %s from DB' % (validity_days,count,title))
    else:
      BluesConsole.success('Fail to remove the dated (more than %s days) materials from DB, error: %s' % (validity_days,message))
