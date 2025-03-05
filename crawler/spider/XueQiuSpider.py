
import subprocess,os,requests,json,time,random,logging

from .baseSpider import BaseSpider


class XueQiuSpider(BaseSpider):
    def __init__(self):
        super().__init__('XueQiu')
        self.datas=[]
        self.new_time = 0


    def run(self,symbol,new_time):
        self.is_running=True
        last_id = ''
        self.new_time = new_time
        self.datas=[]
        count = 100

        referer=f'https://xueqiu.com/S/{symbol}?{self.md5(f'https://xueqiu.com/S/{symbol}')}'
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'connection': 'keep-alive',
            'cookie': f'cookiesu=621569772988355; xqat={random.randint(1,500000)}',
            'elastic-apm-traceparent': '00-20e79fc55e9b4d714bd12ad2f8f991c8-5aeebda2e9f67a7e-00',
            'host': 'xueqiu.com',
            'referer': referer,#是可以变化的最好是爬几次换一个股票代码然后换一个md5再爬
            'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
            'x-requested-with': 'XMLHttpRequest'
        }
        i=1
        while i<count+1:
            if self.is_running is False:
                break

            if last_id=='':
                url = f'https://xueqiu.com/query/v1/symbol/search/status.json?count=10&comment=0&symbol={symbol}&hl=0&source=all&sort=time&page={i}&q=&type=11'
            else:
                url = f'https://xueqiu.com/query/v1/symbol/search/status.json?count=10&comment=0&symbol={symbol}&hl=0&source=all&sort=time&page={i}&q=&type=11&last_id={last_id}'

            url =f'{url}&md5__1038={self.md5(url)}'
            try:
                response = requests.get(url, headers=headers)
    
                if response.status_code == 200:
                    try:
                        t_json=json.loads(response.text)
                        count=t_json['maxPage']
                        last_id = self.json_get(t_json)
                    except:
                        logging.warning(f'获取{symbol}的第{i}页数据网络出现问题')
                logging.info(f"获取了{i}页数据")
                i=i+1
            except :
                time.sleep(60)
        self.is_running=False
        return {'name':'XueQiu','data':self.datas}

    def json_get(self,adata):
        last_id = ''
        for article in adata['list']:
            
            last_id = article['id']
 
                    
            item = {
                "title": article['title'],
                "ID": article['target'],
                "time": article['created_at'],
                "tag": adata['about'],
                "text": article['text']# 将 HTML 转换为 Markdown
            }
            self.datas.append(item)
        if self.new_time>article['created_at']:
            if self.new_time != 0:
                self.is_running=False
        return last_id

    def md5(self,url):
        try:
            result_square = subprocess.run(['node', os.path.join(os.getcwd(), 'crawler/spider/xueqiuwang.js')]+[url], capture_output=True, text=True, check=True)
            return result_square.stdout.strip()
        except subprocess.CalledProcessError as e:
            logging.warning(f"执行 雪球MD5加密 时出错: {e.stderr.strip()}")