import sys,os,re,time
from .AIQA import AIQA
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.moshu.MoshuSchemaFactory import MoshuSchemaFactory
#from sele.loginer.Moshu.MoshuLoginerFactory import MoshuLoginerFactory   

class MoshuQA(AIQA):
  
  def __init__(self,question=''):
    # { AIQASchema }
    schema = MoshuSchemaFactory().create_qa(question)
    # { Loginer } set loginer for relogin
    loginer = None; #MoshuLoginerFactory().create_mac()

    super().__init__(schema,loginer)

  def extract(self,para_rows):
    '''
    Template method: extract title and para list from the text square
    Parameters:
      para_rows {dict} : [{'type':'text','value':'xxx'}]
    '''
    return para_rows

