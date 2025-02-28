import subprocess
import requests
import json

import time
import random
import os
import html2text
import math
import pymongo
class XueQiu():
    def __init__(self):
        self.mongo = MongoDBHelper.MongoDBHelper()
    def json_get(self,adata):
        h = html2text.HTML2Text()
        h.body_width = 0
        last_id = ''
        for article in adata['list']:
            last_id = article['id']
            if self.mongo.check_attribute_exists('XueQiu','ID',article['target']):
                self.mongo.add_tag_if_target_exists_and_tag_not_exists(article['target'],adata['about'])
                print(article['target'])
                continue
            item = {
                "title": article['title'],
                "ID": article['target'],
                "time": article['created_at'],
                "tag": adata['about'],
                "text": h.handle(article['text'])# 将 HTML 转换为 Markdown
            }
            self.mongo.insert_exists('XueQiu',item)
        print('存储一次')
        return last_id
    def md5(self,url):
        try:
            result_square = subprocess.run(['node', os.path.join(os.getcwd(), 'Synthetic-DSS/src/CrawlingModule/xueqiuwang.js')]+[url], capture_output=True, text=True, check=True)
            return result_square.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"执行 雪球MD5加密 时出错: {e.stderr.strip()}")

    def search_articles(self,symbol):
        last_id = ''
        count = 100
        #print(os.path.join(os.getcwd(), 'CrawlingModule/xueqiuwang.js'))
        referer=f'https://xueqiu.com/S/{symbol}?{self.md5(f'https://xueqiu.com/S/{symbol}')}'
        for i in range(1, 10):
            if i > count:
                break
            if last_id=='':
                url = f'https://xueqiu.com/query/v1/symbol/search/status.json?count=10&comment=0&symbol={symbol}&hl=0&source=all&sort=time&page={i}&q=&type=11'
            else:
                url = f'https://xueqiu.com/query/v1/symbol/search/status.json?count=10&comment=0&symbol={symbol}&hl=0&source=all&sort=time&page={i}&q=&type=11&last_id={last_id}'
            headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'connection': 'keep-alive',
                'cookie': 'cookiesu=621739772849353; device_id=8b7c992bcdccaa5e3ac9db3798024bc3; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=; smidV2=20250217141414cb72cb4adb6ca9345ce5809e76aa8144002daa4675a1aac20; s=cl166czzlq; bid=049e676c896fb16a2c838d28a8e11306_m79uoh1h; __utmz=1.1739844819.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=1.1433603976.1739844819.1739844819.1740078970.2; Hm_lvt_1db88642e346389874251b5a1eded6e3=1740103933,1740358543,1740380326,1740444116; HMACCOUNT=766E6D0F15EECEEC; remember=1; xq_a_token=cba667cec1e1e944be18fa20263b63c83caa06e7; xqat=cba667cec1e1e944be18fa20263b63c83caa06e7; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjY0MTU0NDY1NTIsImlzcyI6InVjIiwiZXhwIjoxNzQyNDM0MjAyLCJjdG0iOjE3NDA0NDY3MTA1NzAsImNpZCI6ImQ5ZDBuNEFadXAifQ.BX0yQewkddLSXg4aLpDjZ6spHyCiAQgMMly6SLQZhsVpJBQAglI5ZgEfIe-pWuDGpIowoV5gTB5O_6TCqC2D8N6nHrjytqJOS4ztjxs_aITG6wKiFFrxRGyOc5PFCWyeAhVb27lmWG8hD9flgBPNIOM7mjsntbeJAQ9FGab_4_fwKE_1-V5qJYSnBTaNnPMhCREee3F9w3ldeGT1zZoohSsyPo6FxZjK6zsjc9NpGdT4ti6zaQonD7KqWjjwPVupso083-tx-M_8Za8_zHJMRWUwDvRiFXCOhOI8gku65kN5OWqpNynPTnSIqVJSaIyQzYdVlCcYZrfweNjZpKT35w; xq_r_token=83825858ec5d6d369f5635104c786c88a24f0c59; xq_is_login=1; u=6415446552; snbim_minify=true; acw_tc=ac11000117405324588082850e006b3292da434eb155a5350ee74ec0cb289f; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1740532625; ssxmod_itna=YqRx9DuDBADQi=mK0Lx0pI1Qx2DUxGKYmxwxiUv=p=tD/bvDnqD=GFDK40Eokiv3=KlDRqHernh0GK08BDKxtqCrBxYH=E0O4GLDmKDyYc20eDxEq0rD74irDDxD3SD7PGmDinZuD7xU1S25CfxiOD7eDXxGCDQFhe4Da0gx5=QHqDGHqC90W3DGiDm4CgZc+P9YDnhizC0xCD75Dux0HNWMpDDv6B90sgcSL+S+8oIYDvxDkizH7=82CxUyO+FxFvQxPqA0eK2x4CADx+GGxGWx4bCPoYme5GlG5qhDYInx/CcDDigrbAVDxD==; ssxmod_itna2=YqRx9DuDBADQi=mK0Lx0pI1Qx2DUxGKYmxwxiUv=pxG98oDxBwwuGq7PUKNl7OD6mDv41zleexUKBz7YBDp3=nYBUzG0O3A54=2grxyzPs0oEyzYzeemRCmG8DyDCYi7po0jYIxmwbV2n1Fa5ibh5iNGqiccHkQS7+Oc7TqenCa+0ODanGo8YC/2rA9ZnzdO5vg0eYe7am8oFp5fuwV2Ab+Ywzcr8agWgD97pbq/8wcZEaj8vs3MQjdueTq0+QO2mORBxc9h553nust/noKtG8v=0qZFehEQ/IrV5Ggeu+hTDxqDjhhZ=O7G+l5qQv5EGQZhSYxU2AgQG4Yw/PdeDQZC0viENA3jPo5=wDgPqGmVBPWPvqht/eR2ohArG2aqrrwW0YbgP4ghD6wCS5WAPSntAn5smudcYYDK/mA8AmnP0VWetBT5ITlD4q6Y4rPKEKlCRSYtI1TMWpZnq89E2ooA7YFbwKA61AqYQ3qEGPx49AYzSxBmAUPo2hqiC3dzuP75Pn4DQF3W0OAM=bdNn2q+C=kRDLMCz0q0q+HY1+AtYG=RfQIyAw71l0qD08DijfQjHTwAQ2e3qPYD',
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
            url =f'{url}&md5__1038={self.md5(url)}'
            response = requests.get(url, headers=headers)
 
            if response.status_code == 200:
                t_json=json.loads(response.text)
                count=math.ceil(t_json['count'] / 10)
                last_id = self.json_get(t_json)

            time.sleep(random.randint(1, 5))

if __name__ == "__main__":
    a=XueQiu()
    a.search_articles('SZ002361')