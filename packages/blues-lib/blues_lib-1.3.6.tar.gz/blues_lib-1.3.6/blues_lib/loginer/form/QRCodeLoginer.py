import sys,os,re,time
from abc import ABC,abstractmethod
from datetime import datetime
from .Loginer import Loginer 

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.behavior.BehaviorChain import BehaviorChain
from util.BluesMailer import BluesMailer  
from util.BluesDateTime import BluesDateTime
from util.BluesConsole import BluesConsole

class QRCodeLoginer(Loginer,ABC):
  
  def create_subtype_fields(self):
    # schema extrinsic state
    # { ArrayAtom } the switch atom list
    self.switch_atom = self.schema.switch_atom    
    # { InputAtom } the code input atom 
    self.code_atom = self.schema.code_atom    
    # { int } Verification code expiration seconds
    self.verify_wait_period = self.schema.verify_wait_period_atom.get_value()
    
    #  intrinsic state
    # { int } the last mail sent timestamp 
    self.mail_sent_ts = 0
    # { str } the download QRCode image local file
    self.qrcode_image = ''
  
  # template method
  def perform(self):
    self.switch() 
    self.shot() 
    self.mail()
  
  # === step methods ===
  def switch(self):
    if self.switch_atom:
      handler = BehaviorChain(self.browser,self.switch_atom)
      handler.handle()

  def shot(self):
    '''
    Shot and download the QRCode image
    Returns 
     {str} : the download local file path
    '''
    handler = BehaviorChain(self.browser,self.code_atom)
    outcome = handler.handle()
    print('outcome',outcome)
    if outcome.data:
      self.qrcode_image = outcome.data.get('shot')
      BluesConsole.info('Shot QRcode: %s' % self.qrcode_image)
    else:
      BluesConsole.info('Shot QRcode failurell')
      raise Exception('Shot QRcode failurell')

  def mail(self,ts=None):
    if not self.qrcode_image:
      return

    mailer = BluesMailer.get_instance()
    self.mail_sent_ts = ts if ts else BluesDateTime.get_timestamp()
    para = 'The %s account needs to be re-logged in, please download and scan the QRCode to login within %s seconds.' % (self.domain,self.verify_wait_period)
    content = mailer.get_html_body('NAPS',para)
    payload={
      'subject':mailer.get_title_with_time('NAPS: 视频号登录'),
      'content':content,
      'images':[self.qrcode_image],
      'addressee':['langcai10@dingtalk.com','1771548541@qq.com','118190590@qq.com'], # send to multi addressee
      'addressee_name':'BluesLiu',
    }
    result = mailer.send(payload)
    if result.get('code') == 200:
      BluesConsole.success('Notify email sent successfully')
    else:
      raise Exception('Notify email sent failure')

