import unittest,HTMLTestRunner
from abc import ABC, abstractmethod
#from PlainAtomCase import PlainAtomCase

class TestSuite(ABC):

  def __init__(self):
    self.suite = self.get_suite()


  @abstractmethod
  def get_suite(self):
    '''
    This method is implemented concretely by subclasses
    '''
    pass

  def discover(self):
    '''
    Load test cases by dir and file names
    '''
    return unittest.TestLoader().discover(start_dir='./',pattern='*Case.py')

  def console(self):
    # print log
    unittest.TextTestRunner(verbosity=2).run(self.suite)
  
  def log(self,log_html='./suite-report.html',title='Suite Report',description='Smoke Tests'):
    # write to log file
    steam = open(log_html,'w')
    runner = HTMLTestRunner.HTMLTestRunner(stream=steam,title=title,description=description)
    runner.run(self.suite)


