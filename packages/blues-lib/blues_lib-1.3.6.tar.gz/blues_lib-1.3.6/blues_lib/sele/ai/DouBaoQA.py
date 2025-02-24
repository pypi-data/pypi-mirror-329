import sys,os,re,json
from .AIQA import AIQA
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from model.models.DouBaoModelFactory import DouBaoModelFactory
from loginer.factory.DouBaoLoginerFactory import DouBaoLoginerFactory   
from util.BluesConsole import BluesConsole

class DouBaoQA(AIQA):
  
  def __init__(self,question='',rule=None):
    self.rule = rule if rule else { 'title_length':28 }
    # { AIQASchema }
    material = {'question':question}
    model = DouBaoModelFactory().create_qa(material)
    # { Loginer } set loginer for relogin
    loginer = DouBaoLoginerFactory().create_persistent_mac()

    super().__init__(model['schema'],loginer)

  def extract(self,content):
    # content is text copy from the clip board
    paras = self.__get_para_list(content)
    
    # the first line is the title
    title_para = paras.pop(0)
    title = self.__get_title(title_para)
    
    if not title or not paras:
      return None

    return {
      'paras':json.dumps(paras,ensure_ascii=False),
      'title':title
    }
    
  def __get_para_list(self,content):
    body = content.replace('"',"'")
    paras = re.split(r'[\n\r]', body)
    para_list = []
    for para in paras:
      text = para.strip()
      # sometime the last line is the ai's tip, remove it
      if text and text.find('润色')==-1:
        para_list.append(text)

    return para_list

  def extract2(self,ai_entity):
    '''
    Template method: extract title and para list from the text square
    Parameters:
      ai_entity {dict} : such as {'title':'text','content':'xxx\n\nxxx\n\nxxx'}
    Returns:
      {dict} : {'title':'xxx','paras':'json of text list'}
    '''
    content = ai_entity['content']
    return self.__get_field_dict(content)

  def __get_field_dict(self,content):
    '''
    Returns {json} : json of str list
    '''
    if not content:
      return None

    # remov all " for convert to json
    title_item = content.pop(0)
    title = self.__get_title(title_item['value'])

    if not content:
      return None

    texts = []
    for para_item in content:
      texts.append(para_item['value'])
    
    title_length = self.rule.get('title_length')
    if title_length and title_length<len(title):
      BluesConsole.error('Title too long (max:%s)' % str(title_length))
      return None

    return {
      'paras':json.dumps(texts,ensure_ascii=False),
      'title':title
    }

  def __get_title(self,title):
    # pattern 1 : 标题：《xxx》
    matcheds_01 = re.findall(r'《(.+)》',title)
    # pattern 2: 标题: xxx
    matcheds_02 = re.findall(r'标题\s*[:：]?\s*(.+)',title)
    # If have no title, don't use the ai result
    if matcheds_01:
      text = matcheds_01[0]
    if matcheds_02:
      text = matcheds_02[0]

    # patter : ** xxx **
    text = text.replace('*','')

    title_length = self.rule.get('title_length')
    if title_length and title_length<len(text):
      BluesConsole.error('Title too long (max:%s)' % str(title_length))
      return None

    return text
