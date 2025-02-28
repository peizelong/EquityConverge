
import os
import logging
from spider import JiuYanSpider
from spider import XueQiuSpider
from pipline import Pipline

import json

class crawler():
    def __init__(self):
        
        with open('crawler/config.json', 'r', encoding='utf-8') as file:
            self.config = json.load(file)
        self.pipline = Pipline()
        self.JiuYanSpider = JiuYanSpider.JiuYanSpider()
        self.XueQiuSpider = XueQiuSpider.XueQiuSpider()

    def run(self):

        # self.config['JiuYan']['Last_Time']=self.pipline.get_pipline(self.JiuYanSpider.run(self.config['JiuYan']['Last_Time']))
        # with open('crawler/config.json', 'w') as file:
        #     json.dump(self.config, file)
        # 1555
        for i in range(1238,len(self.config['XueQiu'])):
            logging.info(f'正在获取{self.config['XueQiu'][i]['证券代码']}的帖子')
            data = self.XueQiuSpider.run(self.config['XueQiu'][i]['证券代码'],self.config['XueQiu'][i]['Last_Time'])
            if len(data.get('data', [])) == 0:
                continue
            print(i)
            self.config['XueQiu'][i]['Last_Time']= self.pipline.get_pipline(data)
            with open('crawler/config.json', 'w',encoding='utf-8') as file:
                #print(self.config)
                json.dump(self.config, file,ensure_ascii=False)
        print("完成")

        
        
logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO,
                    filename='test.log',
                    filemode='a',
                    encoding='utf-8')


cra = crawler()
cra.run()






