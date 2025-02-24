import sys,os,re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from .BluesDriver import BluesDriver

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesPowerShell import BluesPowerShell 

class BluesChromeDriver(BluesDriver):

  def __init__(self):
    super().__init__()
    self.arguments = {
      '--start-maximized', # maximize window when open
      '--no-default-browser-check',
      '--disable-notifications',
      '--disable-infobars',
      '--hide-crash-restore-bubble', # 是否打开崩溃前的页面
      '--disable-popup-blocking',
      '--disable-extensions-api', 
      '--disable-application-install-prompt',
      '--no-first-run', 
      '--disable-first-run-ui',
      '--disable-extensions', # 禁用扩展插件
      '--ignore-ssl-errors',
      '--ignore-certificate-errors'
    }
    self.experimental_options = {
      'detach':True, # 设置driver执行完毕后不自动关闭
      'excludeSwitches':['ignore-certificate-errors','enable-automation'], # 屏蔽 ignore提示
      'useAutomationExtension':False, # 去掉"chrome正受到自动化测试软件的控制"的提示条
      'prefs' : {
        'plugins.plugins_disabled':[
          'Chrome PDF Viewer', # 禁用pdf插件
          'Adobe Flash Player' # 禁用flash插件
        ],
        # 0 - Default, 1 - Allow, 2 - Block
        "profile.default_content_setting_values.notification": 2,
        # set the download dir
        'download.default_directory':self.download_dir,
        # Removing the webdriver property from the navigator object,so the browser could not distinguish whether for robots
        "page.addScriptToEvaluateOnNewDocument":{
          "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        }
      }
    }

  def set_selenium_driver(self):
    self.selenium_driver = webdriver

  def set_executable_path(self):
    self.executable_path  = BluesPowerShell.get_env_value('CHROME_DRIVER_EXE')
  
  def set_arguments(self):
    pass

  def set_experimental_options(self):
    pass

  def get(self):
    '''
    @description : Get the web driver instance
    '''
    self.set_selenium_driver()
    self.set_executable_path()
    self.set_arguments()
    self.set_experimental_options()
    chrome_service = self.__get_chrome_service()
    chrome_options = self.__get_chrome_options()
    # 升级selenium 4.25.0后，可以不指定service地址，每次启动会动态安装驱动
    # 类似指定 ChromeDriverManager().install()作为参数
    return self.selenium_driver.Chrome( service = chrome_service, options = chrome_options)

  def __get_chrome_options(self):
    chrome_options = ChromeOptions()
    
    for value in self.arguments:
      chrome_options.add_argument(value)

    for key,value in self.experimental_options.items(): 
      chrome_options.add_experimental_option(key,value)

    return chrome_options

  def __get_chrome_service(self):
    executable_path=self.executable_path if self.executable_path  else ChromeDriverManager().install()
    return ChromeService(executable_path) 



