import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from model.decoder.DecoderHandler import DecoderHandler
from atom.Atom import Atom

class SchemaEntityText(DecoderHandler):
  '''
  Replace the schema's placeholder by data
  '''
  kind = 'handler'

  def resolve(self,request):
    '''
    Parameter:
      request {dict} : the schema and value dict, such as:
        {'atom':Atom, 'value':dict}
    '''
    if not request or not request.get('schema') or not request.get('material'):
      return request
    
    self.__limit_content(request)
    self.__limit_title(request)

    return request

  def __limit_content(self,request):
    '''
    Replace the placeholder value in the atom
    Parameter:
      entity {dict} : the key is the placeholder, the value is the real value
    '''
    limit = request['schema'].limit_atom.get_value()
    material = request['material']
    schema = request['schema']

    # Only support to replace the atom's vlue
    content_max_length = limit.get('content_max_length')

    material_body_text = material.get('material_body_text')
    material_title = material.get('material_title')
    material_type = material.get('material_type')

    if content_max_length and material_body_text:
      # add title to the content in the events channel
      if material_title and schema.CHANNEL=='events' and material_type!='gallery':
        material_body_text.insert(0,'[%s] ' % material_title)

      limit_material_body_text = []
      length = 0
      for para in material_body_text:
        if length<content_max_length:
          # must add a \n to break the line
          line=para
          if schema.CHANNEL=='news':
            line+='\n'

          limit_material_body_text.append(line)
          length += len(line)

      material['material_body_text'] = limit_material_body_text

  def __limit_title(self,request):
    '''
    Replace the placeholder value in the atom
    Parameter:
      entity {dict} : the key is the placeholder, the value is the real value
    '''
    limit = request['schema'].limit_atom.get_value()
    material = request['material']

    # Only support to replace the atom's vlue
    title_max_length = limit.get('title_max_length')
    material_title = material.get('material_title')

    if title_max_length and material_title:
      if len(material_title)>title_max_length:
        end_index = title_max_length-3
        limit_material_title = material_title[:end_index]+'...'
        material['material_title'] = limit_material_title




