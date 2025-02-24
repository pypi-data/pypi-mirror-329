import sys,os,re

from .NAPS import NAPS
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from plan.PublishPlanFactory import PublishPlanFactory     
from model.models.BaiJiaDBModelFactory import BaiJiaDBModelFactory
from loginer.factory.BaiJiaLoginerFactory import BaiJiaLoginerFactory   

class BaiJiaNAPS(NAPS):

  CHANNEL = 'baijia'

  def _get_plan(self):
    return PublishPlanFactory().create_baijia()
    
  def _get_loginer(self):
    loginer_factory = BaiJiaLoginerFactory()
    return loginer_factory.create_account()

  def _get_models(self):
    query_condition = {
      'mode':'latest',
      'count':self._plan.current_total,
    }
    factory = BaiJiaDBModelFactory()
    return factory.create(self._plan.current_quota,query_condition)
