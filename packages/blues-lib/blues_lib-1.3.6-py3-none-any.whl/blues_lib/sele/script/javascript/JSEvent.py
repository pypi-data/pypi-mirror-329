class JSEvent():

  def click(self,selector):
    script = 'document.querySelector("%s").click()' % selector
    self.execute(script)

  
