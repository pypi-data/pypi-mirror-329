import pandas

class BluesCSV():
  
  @classmethod
  def read(cls,csv_file):
    df = pandas.read_csv(csv_file)
    return df

  @classmethod
  def read_head(cls,csv_file):
    '''
    Returns {str} : multi original lines at the beginning
    '''
    df = cls.read(csv_file)
    return df.head()

  @classmethod
  def read_rows(cls,csv_file):
    df = cls.read(csv_file)
    return df.to_dict(orient='records')
