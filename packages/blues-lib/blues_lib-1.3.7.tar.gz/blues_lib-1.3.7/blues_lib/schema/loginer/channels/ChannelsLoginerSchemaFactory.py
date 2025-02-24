import sys,os,re
from .ChannelsQRCodeSchema import ChannelsQRCodeSchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.LoginerSchemaFactory import LoginerSchemaFactory

class ChannelsLoginerSchemaFactory(LoginerSchemaFactory):

  def create_qrcode(self):
    return ChannelsQRCodeSchema()
