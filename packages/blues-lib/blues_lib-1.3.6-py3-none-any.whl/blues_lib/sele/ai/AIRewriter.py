import sys,os,re,json
from .DouBaoQA import DouBaoQA
from .MoshuQA import MoshuQA
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.BluesMaterialIO import BluesMaterialIO     
from util.BluesConsole import BluesConsole

class AIRewriter():
  '''
  This class writer the input news
  '''
  
  def __init__(self,ai_name='doubao',retry_max_count=2):
    '''
    Paramters:
      ai {str} : The ai name 
    '''
    # { AIQA }
    self.ai_name = ai_name
    # {int} the retry count if rewrite fail
    self.retry_max_count = retry_max_count
    self.retry_count = 0
    # {dict}
    self.rule = {
      'title_length':28,
    }

  def get_ai_qa(self,question):
    if self.ai_name=='doubao':
      return DouBaoQA(question,self.rule)
    elif self.ai_name=='moshu':
      return MoshuQA(question)

  def rewrite(self,article,length=500):
    if not article:
      BluesConsole.error('No article for question')
      return

    question = self.get_question(article,length)
    ai_qa = self.get_ai_qa(question)
    entity = ai_qa.execute()

    if not entity:
      if self.retry_count < self.retry_max_count:
        self.retry_count+=1
        BluesConsole.info('Rewrited failure, retry')
        return self.rewrite(article,length)
      else:
        BluesConsole.info('Rewrited failure')
        return None
    else:
      BluesConsole.info('Rewrited successfully: %s' % entity)
      return entity

  def rewrite_by_texts(self,texts,length=500):
    '''
    Parameters:
       texts {json or list} : 
    '''
    article = self.get_article_by_texts(texts)
    return self.rewrite(article,length)

  def rewrite_by_id(self,id='',length=500):
    article = self.get_article_by_id(id)
    return self.rewrite(article,length)

  def get_question(self,article,length=500):
    title_length = str(self.rule['title_length'])
    values = (length,title_length,article)
    q = '帮我对以下内容进行润色，润色要求%s字以内，采用夸张及暗黑手法，分段明确，并提供一个长度在%s字以内的标题党风格的标题: %s' % values
    return q

  def get_article_by_texts(self,texts):
    '''
    Get the rewrite question from the text list
    Parameter:
      texts {json or list} the article's para list
    '''
    paras = texts
    if type(texts) == str:
      paras = json.loads(texts)
    article = ''
    for para in paras:
      article+=para
    return article

  def get_article_by_id(self,id=''):
    '''
    Get a full content from body para list
    '''
    material_body_text = self.get_material(id)
    if not material_body_text:
      return None
    else:
      return self.get_article_by_texts(material_body_text)

  def get_material(self,id=''):
    if id:
      conditions = [
        {'field':'material_id','comparator':'=','value':id}, # ifeng.com_8dZIWYbSBUs 
        {'field':'material_body_text','comparator':'!=','value':''}, 
      ]
      response = BluesMaterialIO.get('*',conditions)
    else:
      response = BluesMaterialIO.random()

    if response['data']:
      texts = response['data'][0]['material_body_text']
      if texts:
        return texts
      else:
        BluesConsole.error('Bad row data,no texts: %s' % response)
        return None

    else:
      BluesConsole.error('No material : %s' % response)
      return None

    


