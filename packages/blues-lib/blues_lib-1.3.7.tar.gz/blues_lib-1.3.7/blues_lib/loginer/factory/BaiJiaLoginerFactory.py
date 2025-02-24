import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.factory.BaiJiaLoginerSchemaFactory import BaiJiaLoginerSchemaFactory
from loginer.factory.LoginerFactory import LoginerFactory
from loginer.OnceLoginer import OnceLoginer   
from loginer.PersistentLoginer import PersistentLoginer   
from loginer.form.AccountLoginerForm import AccountLoginerForm   
from loginer.form.MACLoginerForm import MACLoginerForm   

class BaiJiaLoginerFactory(LoginerFactory):
  def create_once_account(self):
    factory = BaiJiaLoginerSchemaFactory()
    schema = factory.create_account()
    form = AccountLoginerForm(schema)
    return OnceLoginer(schema,form)

  def create_persistent_account(self):
    factory = BaiJiaLoginerSchemaFactory()
    schema = factory.create_account()
    form = AccountLoginerForm(schema)
    return PersistentLoginer(schema,form)

  def create_once_mac(self):
    factory = BaiJiaLoginerSchemaFactory()
    schema = factory.create_mac()
    form = MACLoginerForm(schema)
    return OnceLoginer(schema,form)

  def create_persistent_mac(self):
    factory = BaiJiaLoginerSchemaFactory()
    schema = factory.create_mac()
    form = MACLoginerForm(schema)
    return PersistentLoginer(schema,form)




