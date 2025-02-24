from .Releaser import Releaser

class NewsReleaser(Releaser):
  
  def fill(self):
    self._fill_field('title_atom')
    self._fill_field('content_atom')
    self._fill_field('others_atom')

