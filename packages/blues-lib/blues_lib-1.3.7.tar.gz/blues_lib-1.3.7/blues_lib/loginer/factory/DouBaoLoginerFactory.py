import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.factory.DouBaoLoginerSchemaFactory import DouBaoLoginerSchemaFactory
from loginer.factory.LoginerFactory import LoginerFactory
from loginer.OnceLoginer import OnceLoginer   
from loginer.PersistentLoginer import PersistentLoginer   
from loginer.form.MACLoginerForm import MACLoginerForm   

class DouBaoLoginerFactory(LoginerFactory):

  def create_once_mac(self):
    factory = DouBaoLoginerSchemaFactory()
    schema = factory.create_mac()
    form = MACLoginerForm(schema)
    return OnceLoginer(schema,form)

  def create_persistent_mac(self):
    factory = DouBaoLoginerSchemaFactory()
    schema = factory.create_mac()
    form = MACLoginerForm(schema)
    return PersistentLoginer(schema,form)




