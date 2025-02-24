from .Releaser import Releaser

class EventsReleaser(Releaser):
  
  def fill(self):
    self._fill_field('content_atom')
    self._fill_field('gallery_atom')
    self._fill_field('others_atom')

