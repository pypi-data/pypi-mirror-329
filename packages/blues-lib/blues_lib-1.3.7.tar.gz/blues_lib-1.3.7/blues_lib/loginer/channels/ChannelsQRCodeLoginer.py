import sys,os,re,time
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.behavior.BehaviorChain import BehaviorChain
from sele.loginer.QRCodeLoginer import QRCodeLoginer
from schema.loginer.channels.ChannelsLoginerSchemaFactory import ChannelsLoginerSchemaFactory
from util.BluesDateTime import BluesDateTime

class ChannelsQRCodeLoginer(QRCodeLoginer):

  def create_schema(self):
    factory = ChannelsLoginerSchemaFactory()
    self.schema = factory.create_qrcode()

