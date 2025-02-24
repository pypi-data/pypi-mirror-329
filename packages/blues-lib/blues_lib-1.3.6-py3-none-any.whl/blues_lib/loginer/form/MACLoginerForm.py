import sys,os,re,time
from abc import ABC,abstractmethod
from datetime import datetime
from .LoginerForm import LoginerForm 

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.behavior.BehaviorChain import BehaviorChain
from pool.DBTableIO import DBTableIO
from util.BluesMailer import BluesMailer  
from util.BluesDateTime import BluesDateTime
from util.BluesConsole import BluesConsole
from util.BluesURL import BluesURL

class MACLoginerForm(LoginerForm,ABC):
  
  def __init__(self,schema):
    super().__init__(schema)
    
    # { int } Verification code expiration seconds
    self.captcha_valid_period = self.schema.captcha_valid_period_atom.get_value()
    self.login_page_url = self.schema.login_page_url_atom.get_value()
    # { DBTableIO }
    self.io = DBTableIO('naps_loginer')
    #  { str } the site's main domain
    self.domain = BluesURL.get_main_domain(self.login_page_url)
  
    # { int } the last mail sent timestamp 
    self.mail_sent_ts = 0
    # { str } the dynamic sms auth code
    self.auth_code = ''
  
  # template method
  def perform(self,browser):
    self.browser = browser
    self.before_fill() 
    self.fill() 
    self.send() 
    self.mail()
    self.wait()
    self.before_code() 
    self.code() 
    self.submit() 
  
  # === step methods ===
  def before_fill(self):
    if self.schema.before_fill_atom:
      handler = BehaviorChain(self.browser,self.schema.before_fill_atom)
      handler.handle()

  def fill(self):
    if self.schema.fill_atom:
      handler = BehaviorChain(self.browser,self.schema.fill_atom)
      handler.handle()

  def send(self):
    if self.schema.send_atom:
      handler = BehaviorChain(self.browser,self.schema.send_atom)
      handler.handle()

  def mail(self,ts=None):
    mailer = BluesMailer.get_instance()
    self.mail_sent_ts = ts if ts else BluesDateTime.get_timestamp()
    para = 'The %s account needs to be re-logged in, a verification code has been sent, please upload it within %s seconds.' % (self.domain,self.captcha_valid_period)
    url = 'http://deepbluenet.com/naps-upload-code.html?site=%s&ts=%s' % (self.domain,self.mail_sent_ts)
    url_text = 'Click here to open the upload page.'
    content = mailer.get_html_body('NAPS',para,url,url_text)
    payload={
      'subject':mailer.get_title_with_time('NAPS: Submit the auth code'),
      'content':content,
      'addressee':['langcai10@dingtalk.com'], # send to multi addressee
      'addressee_name':'BluesLiu',
    }
    result = mailer.send(payload)
    if result.get('code') == 200:
      BluesConsole.success('Notify email sent successfully')
    else:
      raise Exception('Notify email sent failure')

  def wait(self):
    '''
    Wait the code upload and continue
    '''
    step = 10
    time_nodes =  list(range(0,self.captcha_valid_period,step)) 
    i = 0
    for time_node in time_nodes:
      i+=1
      auth_code = self.__get_auth_code()
      if auth_code:
        self.auth_code = auth_code
        BluesConsole.success('SMS code ready: %s' % auth_code)
        break

      BluesDateTime.count_down({
        'duration':step,
        'title':'[%s/%s] Wait the auth code' % (str(i*step),str(self.captcha_valid_period))
      })

    if not self.auth_code:
      raise Exception('Timeout: query the auth code failure')

  def before_code(self):
    # add dynamic sms auth code to atom's value
    if self.schema.before_code_atom:
      handler = BehaviorChain(self.browser,self.schema.before_code_atom)
      handler.handle()

  def code(self):
    # add dynamic sms auth code to atom's value
    if self.schema.code_atom:
      self.schema.code_atom.set_value(self.auth_code)
      handler = BehaviorChain(self.browser,self.schema.code_atom)
      handler.handle()

  def submit(self):
    if self.schema.submit_atom:
      handler = BehaviorChain(self.browser,self.schema.submit_atom)
      handler.handle()

  # === tool method ==
  def __get_auth_code(self):
    conditions = [
      {'field':'login_ts','comparator':'=','value':self.mail_sent_ts},
      {'field':'login_site','comparator':'=','value':self.domain},
    ]
    result = self.io.get('*',conditions)
    BluesConsole.info('Wait sms: %s' % result)
    data = result.get('data')
    if data:
      return data[0]['login_sms_code']
    else:
      return None


