import time , json , requests , random,logging
from datetime import datetime





from .baseSpider import BaseSpider

class JiuYanSpider(BaseSpider):
    def __init__(self):
        # Call the constructor of the parent class using super()
        super().__init__('JiuYan')

        self.datas = []

    def run(self,new_time):
        if self.is_running == True:
            return None
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
                    if self.__Get_url_pool(res.json(),new_time)==False:
                        print('已经没有最新的帖子了')
                        break
                else:
                    logging.warning(f'服务器拒绝链接{res.json()['msg']}')
            else:
                
                print(f"url请求失败，状态码: {res.status_code}")
            time.sleep(random.uniform(1, 10))
            
        logging.info(f'XueQiu最新文章提取完成,共{len(self.datas)}篇')
        # 提取链接内的文章
        #print(self.datas)
        for i in range(len(self.datas)):
            self.datas[i]['text'] = self.__extract_content(self.datas[i]['ID'])
            #print(self.datas[i]['text'])
            time.sleep(random.uniform(1, 10))
        self.is_running=False


        w = {'name':self.name,'data':self.datas}
        return w

    def __Get_url_pool(self,adata,new_time)->bool:
        if adata['data']['result'] == '':
            return False
        for article in adata['data']['result']:
            tags = [stock['code'] for stock in article['stock_list']]
            #print (article['create_time'])
            now_time = datetime.strptime(article['create_time'], "%Y-%m-%d %H:%M:%S").timestamp()*1000
            if new_time > now_time :#对比数据库最新的时间，如果没有超过最新时间即存入date_str2=self.new_time
                return False
            item = {
                "title": article['title'],
                "ID": article['article_id'],
                "time": now_time,
                "tag": tags,
                "text": ''
            }
            self.datas.append(item)
            
    def __extract_content(self,url):
        try:
            # 设置请求头
            headers = {
    #            ":authority": "www.jiuyangongshe.com",
    #            ":method": "GET",
    #            ":path": f"/a/{url}",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
            }
            # 发送请求
            #print(url)
            response = requests.get(f"https://www.jiuyangongshe.com/a/{url}", headers=headers)
            if response.status_code == 200:
               # print(response.text)
                return response.text                
            else:
                print(f"https://www.jiuyangongshe.com/a/{url}")
                print(f"请求失败，状态码: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"请求出现错误: {e}")
            return None