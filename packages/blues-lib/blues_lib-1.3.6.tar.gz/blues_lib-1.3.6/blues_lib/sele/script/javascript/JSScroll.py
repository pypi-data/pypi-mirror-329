class JSScroll():
  
  # == module 1 : scroll x and y == #
  def scroll_x(self,left):
    '''
    @description : scroll along the X-axis
    @param {int} left : the offset tos selector's left border
    '''
    script = "window.scrollTo(%s,0);" % left
    return self.execute(script)
  
  def scroll_y(self,top):
    '''
    @description : scroll along the X-axis
    @param {int} top : the offset tos selector's left border
    '''
    script = "window.scrollTo(0,%s);" % top
    return self.execute(script)

  def scroll_bottom(self):
    '''
    @description : scroll the document to bottom
    '''
    size = self.get_document_size()
    self.scroll_y(size['height'])

  def scroll_top(self):
    '''
    @description : scroll the document to top
    '''
    self.scroll_y(0)
  
  def lazy_scroll_bottom(self,step=500,interval=1000):
    '''
    @description : scroll the page to the bottom, support the content was loaded lazy
    @param {int} step : the scroll height one time
    @param {int} interval : the wait time afater scroll
    '''
    js_script='''
    // 最后一个参数是python程序自动传入的回调
    var callback = arguments[arguments.length-1];
    (function(){
      var scrollHeight = document.body.scrollTop; // 当前滚动条位置
      var step = %s;
      var interval = %s;
      function scroll(){
        // 与最新内容高度比较
        if(scrollHeight<document.body.scrollHeight-window.innerHeight){
          scrollHeight += step;
          window.scroll(0,scrollHeight);
          document.title = scrollHeight;
          setTimeout(scroll,interval);
        }else{
          window.scroll(0,scrollHeight);
          document.title = scrollHeight;
          // 必须显式回调结束程序，否则程序会超时异常
          callback(scrollHeight);
        }
      }
      // 使用setTimeout程序是必须用异步函数，否则浏览器不会等待程序执行完毕就关闭
      setTimeout(scroll,interval);
    })();
    ''' % (step,interval)
    # 返回值是callback抛出值
    return self.execute_async_script(js_script)

  # == module 2 : scroll element to window == #
  def scroll_to_view(self,selector):
    script = 'document.querySelector(`%s`).scrollIntoView(true);' % selector
    self.execute(script)
