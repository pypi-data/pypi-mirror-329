import sys,os,re
from .CleanupHandler import CleanupHandler
from .handler.MaterialUpdater import MaterialUpdater  
from .handler.LogUpdater import LogUpdater  
from .handler.FileCleaner import FileCleaner  
from .handler.DBCleaner import DBCleaner  
from .handler.Notifier import Notifier  

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
#from sele.cleanup.deco.SchemaCleanupHandlerDeco import SchemaCleanupHandlerDeco

class CleanupChain(CleanupHandler):
  '''
  Basic behavior chain, it's a handler too
  '''
  kind = 'chain'

  #@SchemaCleanupHandlerDeco()
  def resolve(self,request):
    '''
    Deal the atom by the event chain
    '''
    handler = self.__get_chain()
    return handler.handle(request)

  def __get_chain(self):
    '''
    Converters must be executed sequentially
    '''
    # writer
    material_updater = MaterialUpdater()
    log_updater = LogUpdater()
    file_cleaner = FileCleaner()
    db_cleaner = DBCleaner()
    notifier = Notifier()
    
    material_updater.set_next(log_updater) \
      .set_next(file_cleaner) \
      .set_next(db_cleaner) \
      .set_next(notifier)

    return material_updater
