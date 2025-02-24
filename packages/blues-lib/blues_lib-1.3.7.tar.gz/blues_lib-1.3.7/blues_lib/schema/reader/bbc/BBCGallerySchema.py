import sys,re,os
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.reader.GalleryReaderSchema import GalleryReaderSchema

class BBCGallerySchema(GalleryReaderSchema):
 pass 
