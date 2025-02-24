from .TouTiaoAccountLoginer import TouTiaoAccountLoginer   

class BluesLoginerFactory():

  def create_account_loginer(self):
    return TouTiaoAccountLoginer()

  def create_mac_loginer(self):
    pass
