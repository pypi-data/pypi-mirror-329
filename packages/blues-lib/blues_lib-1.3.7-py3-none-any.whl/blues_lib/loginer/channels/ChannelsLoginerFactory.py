import sys,os,re
from .ChannelsQRCodeLoginer import ChannelsQRCodeLoginer   
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.loginer.LoginerFactory import LoginerFactory

class ChannelsLoginerFactory(LoginerFactory):

  def create_qrcode(self,once=False):
    return ChannelsQRCodeLoginer(once)
