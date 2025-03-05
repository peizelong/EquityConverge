
import time,random,threading
import logging
from .spider import JiuYanSpider
from .spider import XueQiuSpider
from .pipline import Pipline

import json

class crawler():
    def __init__(self):
        
        with open('crawler/config.json', 'r', encoding='utf-8') as file:
            self.config = json.load(file)
        self.pipline = Pipline()

        

    def run(self):
        #self.XueQiu()
        JYthread=threading.Thread(target=self.__JiuYan)
        XQthread=threading.Thread(target=self.__XueQiu)
        JYthread.start()
        XQthread.start()
        # 1555

    def __JiuYan(self):
        while True:
            JYSpider = JiuYanSpider.JiuYanSpider()
            data = JYSpider.run(self.config['JiuYan']['Last_Time'])
            if len(data.get('data', [])) != 0:

                self.config['JiuYan']['Last_Time']=self.pipline.get_pipline(data)
                with open('crawler/config.json', 'w',encoding='utf-8') as file:
                    json.dump(self.config, file,ensure_ascii=False)
            
            time.sleep(3600)

    def __XueQiu(self):
        XQSpider = XueQiuSpider.XueQiuSpider()
        for i in range(0,len(self.config['XueQiu'])):
            logging.info(f'正在获取{self.config['XueQiu'][i]['股票代码']}的帖子')
            data = XQSpider.run(self.config['XueQiu'][i]['股票代码'],self.config['XueQiu'][i]['Last_Time'])
            if len(data.get('data', [])) == 0:
                continue
            print(i)
            self.config['XueQiu'][i]['Last_Time']= self.pipline.get_pipline(data)

            with open('crawler/config.json', 'w',encoding='utf-8') as file:
                json.dump(self.config, file,ensure_ascii=False)
            time.sleep(random.random())
        print("完成")

        


    def get_one(self,code):
        XueQiu = XueQiuSpider.XueQiuSpider()
        # 获取雪球
        for i in range(0,len(self.config['XueQiu'])):
            if self.config['XueQiu'][i]['股票代码'][2:] == code:

                logging.info(f'正在获取{self.config['XueQiu'][i]['股票代码']}的帖子')
                data = XueQiu.run(self.config['XueQiu'][i]['股票代码'],self.config['XueQiu'][i]['Last_Time'])
                if len(data.get('data', [])) == 0:
                    continue
                print(i)
                self.config['XueQiu'][i]['Last_Time']= self.pipline.get_pipline(data)

                with open('crawler/config.json', 'w',encoding='utf-8') as file:
                    json.dump(self.config, file,ensure_ascii=False)
                time.sleep(random.uniform(1,5))
        print("完成")
        
        

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cra = crawler()
    cra.run()






