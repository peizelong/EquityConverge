from spider.JiuYan import JiuYan

import threading


class Spider_Controller():
    def __init__(self):
        self.JiuYan_spider = JiuYan()
    def run(self):
        self.JiuYan_spider.run()
        #JiuYan_thread = threading.Thread(target=self.JiuYan_spider.run())
            




a=Spider_Controller()
a.run()