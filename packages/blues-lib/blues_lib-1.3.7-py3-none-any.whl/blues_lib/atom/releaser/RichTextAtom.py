from .ReleaserAtom import ReleaserAtom

class RichTextAtom(ReleaserAtom):

  _kind = 'richtext' 

  def __init__(self,title,selector,value,selector_template=''):
    '''
    A complex atom for rich text, contains a text atom list and a image atom list
    Parameter:
      title (str) : the atom's description
      selector (str) : the data parent selector
      value (ValueAtom) : a complex dict value , contains:
        - image_atom {ArrayAtom}
        - text_atom {ArrayAtom}
        - entity {ValueAtom} : if set this attr, 
          - it set a placeholder ${xxx} to receive the list of texts and images
          - or, the top atom set placehoder themself
   Returns:
      BluesAtom : a atom instance
    '''
    super().__init__(self._kind,title,selector,value,selector_template)
