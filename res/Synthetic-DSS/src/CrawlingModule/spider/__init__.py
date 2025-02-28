#@from spider.JiuYan import JiuYan

class spider():
    def __init__(self,name):
        self.is_running = False
        self.name = name
    def run(self):
        self.is_running = True
        self.crawl()
    def crawl(self):
        pass
