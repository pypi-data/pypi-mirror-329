import pyperclip

class BluesOS():
  
  @classmethod
  def copy(cls):
    # copy from the os's clip board
    return pyperclip.paste()