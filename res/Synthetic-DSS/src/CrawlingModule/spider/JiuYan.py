
import requests
import time
import logging
import random
import configparser
from datetime import datetime
import json

from . import spider

proxy = {
    'http': 'http://202.101.213.42',  # HTTP 代理
    'https': 'https://202.101.213.42'  # HTTPS 代理
}

class JiuYan(spider):  
    
    url_pool=[] 
    def __init__(self):
        spider().__init__='JiuYan'
        self.config = configparser.ConfigParser()
        self.config.read('spider_config.ini')
        self.new_time =self.config['spider']["last_time"]

    def crawl(self):
        i=0
        while True:

            url ="https://app.jiuyangongshe.com/jystock-app/api/v2/article/community"

            data = {
                'is_newest': '1',
                'order': '0',
                'limit': '15',
                'start': str(i+1),
                'type': '0'
            }
            current_timestamp = int(time.time() * 1000)
            headers = {
                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "content-type": "application/json",
                "origin": "https://www.jiuyangongshe.com",
                "platform": "3",
                "referer": "https://www.jiuyangongshe.com/",
                "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Microsoft Edge\";v=\"133\", \"Chromium\";v=\"133\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "timestamp": str(current_timestamp),
                "token": "e5f0b420fc516761b94f0179db36b5af",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
            }

            json_data = json.dumps(data)
            #请求方式 post
            res = requests.post(url,data=json_data,headers=headers)
            
            if res.status_code == 200:
                if res.json()['msg'] == '':
                        i=i+1
                        if self.__Get_url_pool(res.json())==False:
                            print('已经没有最新的帖子了')
                            break
                else:
                    logging.warning(f'服务器拒绝链接{res.json()['msg']}')
            else:
                print(f"请求失败，状态码: {res.status_code}")
            time.sleep(random.random(1,5))
        self.is_running=False
        self.config.set('JiuYan', 'last_time')
        with open('spider_config.ini', 'w') as configfile:
            self.config.write(configfile)
        return self.url_pool

    
    def __Get_url_pool(self,adata):

        for article in adata['data']['result']:
            tags = [stock['code'] for stock in article['stock_list']]

            if self.new_time >datetime.strptime(article['create_time'], "%Y-%m-%d %H:%M:%S").timestamp()*1000: #对比数据库最新的时间，如果没有超过最新时间即存入date_str2=self.new_time
                print('超过时间')
                return False
            item = {
                "title": article['title'],
                "ID": article['article_id'],
                "time": datetime.strptime(article['create_time'], "%Y-%m-%d %H:%M:%S").timestamp()*1000,
                "tag": tags,
                "text": self.__extract_content(+article['article_id'])
            }
            self.url_pool.append(item)


        return True

    def __extract_content(self,url):
        try:
            # 设置请求头
            headers = {
                ":authority": "www.jiuyangongshe.com",
                ":method": "GET",
                ":path": f"/a/{url}",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
            }
            # 发送请求
            response = requests.get(f"https://www.jiuyangongshe.com/a/{url}", headers=headers)
            if response.status_code == 200:
                return response.text                
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"请求出现错误: {e}")
            return None
    




    # def search_articles(self,keyword, limit=15, start=0):
    #     url = "https://app.jiuyangongshe.com/jystock-app/api/v2/article/search"
    #     data = {
    #         'back_garden': '0',
    #         'keyword': keyword,
    #         'order': '1',
    #         'limit': str(limit),
    #         'start': str(start),
    #         'type': '1'
    #     }
    #     # 获取当前时间戳（毫秒级）
    #     current_timestamp = int(time.time() * 1000)
    #     headers = {
    #         "accept": "application/json, text/plain, */*",
    #         "accept-encoding": "gzip, deflate, br, zstd",
    #         "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    #         "content-type": "application/json",
    #         "origin": "https://www.jiuyangongshe.com",
    #         "platform": "3",
    #         "referer": "https://www.jiuyangongshe.com/",
    #         "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Microsoft Edge\";v=\"133\", \"Chromium\";v=\"133\"",
    #         "sec-ch-ua-mobile": "?0",
    #         "sec-ch-ua-platform": "\"Windows\"",
    #         "sec-fetch-dest": "empty",
    #         "sec-fetch-mode": "cors",
    #         "sec-fetch-site": "same-site",
    #         "timestamp": str(current_timestamp),
    #         "token": "83eeac89e55c2a258a0a66a5ae6078e9",
    #         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
    #     }
    #     json_data = json.dumps(data)
    #     # 请求方式 post
    #     res = requests.post(url, data=json_data, headers=headers,proxies=proxy)

    #     if res.status_code == 200:
    #         # 打印响应内容
    #         #print(res.json())
    #         return self.json_get(res.json())
    #     else:
    #         print(f"请求失败，状态码: {res.status_code}")
    #         return None
        ###


