import re
from bs4 import BeautifulSoup
import html2text
import pymongo
class Pipline():
    def __init__(self):
        self.h = html2text.HTML2Text()
        self.h.body_width = 0
        self.client = pymongo.MongoClient('localhost', 27017)  # 可根据实际情况修改主机和端口
        self.db = self.client['ECSystem']  # 数据库名
        
       
    def get_pipline(self,id):
        if id != None:
            match id['name']:
                case'JiuYan':return self.JiuYan_pipline(id['data'])
                case'XueQiu':return self.XueQiu_pipline(id['data'])

    def JiuYan_pipline(self,datas):
        collection = self.db['JiuYan']  # 集合名
        print(1)

        for data in datas:
            query = {'ID': data['ID']}
            result = collection.find_one(query)
            if  result is not None:
                print(2)
                continue
            soup = BeautifulSoup(data['text'], 'html.parser')
            #print(data)
            script_tag = None
            for script in soup.find_all('script'):
                if 'window.__NUXT__' in script.text:
                    script_tag = script
                    break
            
            pattern = r'content:(.*?),url|,stock_list'

            #print(script_tag)
            matches = re.findall(pattern, script_tag.text)
            #print(url)
            data_str = matches[0]

            unescaped_str = data_str.encode('raw_unicode_escape').decode('unicode_escape')
            # 将 HTML 转换为 Markdown
            
            markdown = self.h.handle(unescaped_str)
            item = {
                "title": data['title'],
                "ID": data['ID'],
                "time": data['time'],
                "tag": data['tag'],
                "text": markdown
            }
            collection.insert_one(item)
            return datas[1]['time']
        
    def XueQiu_pipline(self,datas):
        
        collection = self.db['XueQiu']
        for data in datas:
            query = {'ID': data['ID']}
            result = collection.find_one(query)
            if  result is not None:
                continue
            item = {
                "title": data['title'],
                "ID": data['ID'],
                "time": data['time'],
                "tag": data['tag'],
                "text": self.h.handle(data['text'])
            }
            collection.insert_one(item)
        #print(datas[0]['time'])
        return datas[0]['time']
        