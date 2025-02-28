
class BaseSpider:
    def __init__(self,name):
        self.name  =  name
        self.is_running = False


    def stop(self):
        """
        停止爬虫
        """
        if self.is_running:
            self.is_running = False
    
    def run(self):
        """
        运行爬虫的主方法，需要在子类中实现具体逻辑
        """
        print(1)
        
    def get_is_running(self):
        return self.is_running