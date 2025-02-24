
# plain atoms
from .plain.DataAtom import DataAtom
from .plain.PauseAtom import PauseAtom
from .plain.RegexpAtom import RegexpAtom
from .plain.URLAtom import URLAtom

# event atoms
from .event.ElementAtom import ElementAtom
from .event.ClickableAtom import ClickableAtom
from .event.FrameAtom import FrameAtom
from .event.RollinAtom import RollinAtom
from .event.PopupAtom import PopupAtom

# writer atoms
from .writer.InputAtom import InputAtom
from .writer.InputCharAtom import InputCharAtom
from .writer.TextAreaAtom import TextAreaAtom
from .writer.JSCssAtom import JSCssAtom
from .writer.JSTextAtom import JSTextAtom
from .writer.JSTextAreaAtom import JSTextAreaAtom
from .writer.FileAtom import FileAtom
from .writer.ChoiceAtom import ChoiceAtom
from .writer.SelectAtom import SelectAtom

# releaser
from .releaser.RichTextAtom import RichTextAtom

# reader atoms
from .reader.AttrAtom import AttrAtom
from .reader.TextAtom import TextAtom
from .reader.ValueAtom import ValueAtom
from .reader.CssAtom import CssAtom
from .reader.ShotAtom import ShotAtom

# composite
from .composite.ArrayAtom import ArrayAtom
from .composite.MapAtom import MapAtom

# spider atoms
from .spider.BriefAtom import BriefAtom
from .spider.NewsAtom import NewsAtom
from .spider.ParaAtom import ParaAtom

class AtomFactory():

  # create plain Atoms
  def createData(self,title,value):
    return DataAtom(title,value)

  def createPause(self,title,value=5):
    return PauseAtom(title,value)

  def createRegexp(self,title,value):
    return RegexpAtom(title,value)

  def createURL(self,title,value):
    return URLAtom(title,value)

  # create event Atoms
  def createElement(self,title,selector,value=None,parent_selector=None,timeout=5,selector_template=None):
    return ElementAtom(title,selector,value,parent_selector,timeout,selector_template)

  def createRollin(self,title,selector,value=None,parent_selector=None,timeout=5,selector_template=None):
    return RollinAtom(title,selector,value,parent_selector,timeout,selector_template)

  def createPopup(self,title,selector,value=None,parent_selector=None,timeout=5,selector_template=None):
    return PopupAtom(title,selector,value,parent_selector,timeout,selector_template)

  def createClickable(self,title,selector,value=None,parent_selector=None,timeout=5,selector_template=None):
    return ClickableAtom(title,selector,value,parent_selector,timeout,selector_template)

  def createFrame(self,title,selector,value='in',parent_selector=None,timeout=5,selector_template=None):
    return FrameAtom(title,selector,value,parent_selector,timeout,selector_template)
  
  # create writer Atoms
  def createInputChar(self,title,selector,value=None,interval=1,mode='append',parent_selector=None,timeout=5,selector_template=None):
    return InputCharAtom(title,selector,value,interval,mode,parent_selector,timeout,selector_template)

  def createInput(self,title,selector,value=None,parent_selector=None,timeout=5,selector_template=None):
    return InputAtom(title,selector,value,parent_selector,timeout,selector_template)

  def createTextArea(self,title,selector,value=None,LF_count=1,parent_selector=None,timeout=5,selector_template=None):
    return TextAreaAtom(title,selector,value,LF_count,parent_selector,timeout,selector_template)

  def createJSCss(self,title,selector,value=None,parent_selector=None,timeout=5,selector_template=None):
    return JSCssAtom(title,selector,value,parent_selector,timeout,selector_template)

  def createJSText(self,title,selector,value=None,parent_selector=None,timeout=5,selector_template=None):
    return JSTextAtom(title,selector,value,parent_selector,timeout,selector_template)

  def createJSTextArea(self,title,selector,value=None,LF_count=1,parent_selector=None,timeout=5,selector_template=None):
    return JSTextAreaAtom(title,selector,value,LF_count,parent_selector,timeout,selector_template)

  def createFile(self,title,selector,value=None,wait_time=5,parent_selector=None,timeout=5,selector_template=None):
    return FileAtom(title,selector,value,wait_time,parent_selector,timeout,selector_template)

  def createSelect(self,title,selector,value=True,parent_selector=None,timeout=5,selector_template=None):
    return SelectAtom(title,selector,value,parent_selector,timeout,selector_template)

  def createChoice(self,title,selector,value=True,parent_selector=None,timeout=5,selector_template=None):
    return ChoiceAtom(title,selector,value,parent_selector,timeout,selector_template)
  
  # releaser atoms
  def createRichText(self,title,selector,value=True,selector_template=None):
    return RichTextAtom(title,selector,value,selector_template)

  # reader atoms
  def createText(self,title,selector,value=None,parent_selector=None,timeout=5,selector_template=None):
    return TextAtom(title,selector,value,parent_selector,timeout,selector_template)

  def createValue(self,title,selector,value=None,parent_selector=None,timeout=5,selector_template=None):
    return ValueAtom(title,selector,value,parent_selector,timeout,selector_template)

  def createAttr(self,title,selector,value=None,parent_selector=None,timeout=5,selector_template=None):
    return AttrAtom(title,selector,value,parent_selector,timeout,selector_template)

  def createShot(self,title,selector=None,value=None,parent_selector=None,timeout=5,selector_template=None):
    return ShotAtom(title,selector,value,parent_selector,timeout,selector_template)

  def createCss(self,title,selector,value=None,parent_selector=None,timeout=5,selector_template=None):
    return CssAtom(title,selector,value,parent_selector,timeout,selector_template)
  
  # composite atoms
  def createArray(self,title,value=None,pause=1):
    return ArrayAtom(title,value,pause)

  def createMap(self,title,value=None,pause=1):
    return MapAtom(title,value,pause)

  # spider atoms
  def createPara(self,title,selector,value):
    return ParaAtom(title,selector,value)

  def createBrief(self,title,selector,value):
    return BriefAtom(title,selector,value)

  def createNews(self,title,selector,value):
    return NewsAtom(title,selector,value)
