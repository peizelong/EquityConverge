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
        self.datass=[]
    def to_txt (self):
        pass
    def json_get(self,adata):
        h = html2text.HTML2Text()
        h.body_width = 0
        last_id = ''
        for article in adata['list']:
            last_id = article['id']
            item = {
                "title": article['title'],
                "ID": article['target'],
                "time": article['created_at'],
                "tag": adata['about'],
                "text": h.handle(article['text'])# 将 HTML 转换为 Markdown
            }
            with open('data.json', 'a', encoding='utf-8') as file:
                json.dump(item, file, ensure_ascii=False, indent=4)
        #print('存储一次')
        return last_id
    def md5(self,url):
        #print(os.path.join(os.getcwd(), 'a/xueqiuwang.js'))
        try:
            result_square = subprocess.run(['node', os.path.join(os.getcwd(), 'xueqiuwang.js')]+[url], capture_output=True, text=True, check=True)
            return result_square.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"执行 雪球MD5加密 时出错: {e.stderr.strip()}")

    def search_articles(self,symbol):
        last_id = ''
        count = 100
        #print(os.path.join(os.getcwd(), 'CrawlingModule/xueqiuwang.js'))
        referer=f'https://xueqiu.com/S/{symbol}?{self.md5(f'https://xueqiu.com/S/{symbol}')}'
        for i in range(1, 2):
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
                'cookie': 'cookiesu=621739772849353; device_id=8b7c992bcdccaa5e3ac9db3798024bc3; smidV2=20250217141414cb72cb4adb6ca9345ce5809e76aa8144002daa4675a1aac20; s=cl166czzlq; bid=049e676c896fb16a2c838d28a8e11306_m79uoh1h; __utmz=1.1739844819.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); HMACCOUNT=766E6D0F15EECEEC; snbim_minify=true; __utmc=1; __utma=1.1433603976.1739844819.1740543630.1740640295.4; xq_a_token=55d5135321462c545489a47de10df4ea66183cbf; xqat=55d5135321462c545489a47de10df4ea66183cbf; xq_r_token=446bc022d20d8f70ce374500a1e0112d1edebcfa; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTc0MjE3MzAzNywiY3RtIjoxNzQwNjQ3NzcwMzc0LCJjaWQiOiJkOWQwbjRBWnVwIn0.SdVh40kcfvEUnR5zxzOci7KrowKM7MrwsTLxQ9jsAwvHunLoXzEZYUxLJG3zahIpII1KUzOVDw3K900MjHSNBF4yg2wdir79nq4lPGNRS2RzlLlr-Je0zjjX7F82I0X4E0JdyGBLzb2Z7A36bSj2pg5YQOg-KtOZuiH6dacjBNLj4yXz6l7okbMPcAROhR9UBP7XIh0fElBkGfQusMD0Zep3xV6nBhaWNTSHlKSe__2vRa_52VX5AgFF-TdSQoi_3E8L4oDb6IFc5VVeqWTF0DvgRZfxK9oSxddh5csXuc42ADzHsbxxsJ3p7uhiZsMw873ve2rBnDypjdydzUmiuw; u=621739772849353; Hm_lvt_1db88642e346389874251b5a1eded6e3=1740647811; acw_tc=1a0c66d917407060355757961e003783ffefb464df5b6cca34e96a427f65e0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1740706079; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=b2zZZhBLnKfpE8WyzHfEMixeFqtL3wjQPmidbPQ+mOPk05LeMIwdBZcNQvpiG0RVDuuy9IgCgaYugRufZQ/u7A%3D%3D; ssxmod_itna=QqGxnDgDcA0=G=G7DhPHI5ijY7j5DvKDXDUqAjQGgDYq7=GFDmx0P8pa2AKq+K+xe2e+0GA7=+pqDsrWY4GzDiMPGhDBmAHK/iYyqs3+7hgrerRPmDT4Ca9Ah4pHWfF6p79OyZQGLDmKDU=ibrlGYDemaDCeDQxirDD4DA7PDFxibDinp54Ddi8EIC4E+IDGrDlKDR2hom4Dai9ieeQoxDG5xSbie2lxD4xi3iIEsf845DiyDO3KmD7H3Dlp4bHdD0=1celOIQdF03EYfA40OD0ILH4Y5uQOAkz70KOGb2WWH/3bCrQiesimslG+eqGiDP7Gx=GxmqqBG7AGxGx4o++CIUDDARxXR2O0TP5mYKvgb5mFHMe25Q4VlPT7R5AwYKDbz0xxrqii56BtSrNlaq/Gi954i0Dr+4b4xeD; ssxmod_itna2=QqGxnDgDcA0=G=G7DhPHI5ijY7j5DvKDXDUqAjQGgDYq7=GFDmx0P8pa2AKq+K+xe2e+0GA7=+o4DW+KnirU7q+D7pYeYAG8jYr/BPxD/YicDcxq4VRCeuAaNGSvuEoTt++YwEbKA8e2ZRauPrQKehT2AFhyPwFKAAG3eHH8=GxdzcOUPEF27PYhP7aXZ+4s3uIfZiqW69O189LHfIhlrH6yIHUmKOeNB8QDTMdxfD46zcqdKBTB/+eUFPKfZ2CZEy8mx6f49fENHPOhS6n0Fd0EblC4zt+sID4RZ2RGVbLTE9hU9DEE1sSlRvYFHiaQRRuKDMjFynmQm52mvQCuVt70BWUUHqp90fY5ac9BbObTGeRg9Kztwz9K0B2znBDFF3PWa/iF4u2mwknw6Q0CAP/jex4wP94PqTQmHQ/E+3fWtybdqTPasI3imTX4q0Bbs0nBC+a3ndwwTepgzwFim3oSOS778PZFdO6cDWnDsGpfT7v95iS6R50S+MA44IwdkHxNHM4+OQmz8Q//5pi7qeunKA+UuWTPOtCaGvzm5euFaWk/DHhWCaG784l0Wmv9orhjM7q/jM0t8f=gkf+plcsa0fUPcz2cFd=NMi=UL07M3IWhT0A4Lnyndkfbp=u7FqE+qWCtmnk5m8R4G+GaMalxatKrkmwYlq/mH9aSP+Fi0l64x8S1j0Cie2hwnDeaExGeIxe5ZuMOP4xklqsbz0DKAq8dH2Wi1ZaxjPQiOBQP4mCY4HKSYN+u0G84Ni3YG8ODv+0o7LBOn+2xLY4ZHxhDY0iZqtDra7ePz=KTbN/+2BSOGB27nKP7HlDzPwiWaIxIOHhpaiaoT/dwxZiWZahnesGrmqgikmqMiNnqdaqlx4rORq+D4Y4wieYDD',
                #'elastic-apm-traceparent': '00-20e79fc55e9b4d714bd12ad2f8f991c8-5aeebda2e9f67a7e-00',
                #'host': 'xueqiu.com',
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
            headers2 = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "cache-control": "no-cache",
                "connection": "keep-alive",
                "cookie": "cookiesu=621739772849353; device_id=8b7c992bcdccaa5e3ac9db3798024bc3; smidV2=20250217141414cb72cb4adb6ca9345ce5809e76aa8144002daa4675a1aac20; s=cl166czzlq; bid=049e676c896fb16a2c838d28a8e11306_m79uoh1h; __utmz=1.1739844819.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); HMACCOUNT=766E6D0F15EECEEC; snbim_minify=true; __utmc=1; __utma=1.1433603976.1739844819.1740543630.1740640295.4; xq_a_token=55d5135321462c545489a47de10df4ea66183cbf; xqat=55d5135321462c545489a47de10df4ea66183cbf; xq_r_token=446bc022d20d8f70ce374500a1e0112d1edebcfa; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTc0MjE3MzAzNywiY3RtIjoxNzQwNjQ3NzcwMzc0LCJjaWQiOiJkOWQwbjRBWnVwIn0.SdVh40kcfvEUnR5zxzOci7KrowKM7MrwsTLxQ9jsAwvHunLoXzEZYUxLJG3zahIpII1KUzOVDw3K900MjHSNBF4yg2wdir79nq4lPGNRS2RzlLlr-Je0zjjX7F82I0X4E0JdyGBLzb2Z7A36bSj2pg5YQOg-KtOZuiH6dacjBNLj4yXz6l7okbMPcAROhR9UBP7XIh0fElBkGfQusMD0Zep3xV6nBhaWNTSHlKSe__2vRa_52VX5AgFF-TdSQoi_3E8L4oDb6IFc5VVeqWTF0DvgRZfxK9oSxddh5csXuc42ADzHsbxxsJ3p7uhiZsMw873ve2rBnDypjdydzUmiuw; u=621739772849353; Hm_lvt_1db88642e346389874251b5a1eded6e3=1740647811; acw_tc=1a0c66d917407060355757961e003783ffefb464df5b6cca34e96a427f65e0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1740706079; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=b2zZZhBLnKfpE8WyzHfEMixeFqtL3wjQPmidbPQ+mOPk05LeMIwdBZcNQvpiG0RVDuuy9IgCgaYugRufZQ/u7A%3D%3D; ssxmod_itna=QqGxnDgDcA0=G=G7DhPHI5ijY7j5DvKDXDUqAjQGgDYq7=GFDmx0P8pa2AKq+K+xe2e+0GA7=+pqDsrWY4GzDiMPGhDBmAHK/iYyqs3+7hgrerRPmDT4Ca9Ah4pHWfF6p79OyZQGLDmKDU=ibrlGYDemaDCeDQxirDD4DA7PDFxibDinp54Ddi8EIC4E+IDGrDlKDR2hom4Dai9ieeQoxDG5xSbie2lxD4xi3iIEsf845DiyDO3KmD7H3Dlp4bHdD0=1celOIQdF03EYfA40OD0ILH4Y5uQOAkz70KOGb2WWH/3bCrQiesimslG+eqGiDP7Gx=GxmqqBG7AGxGx4o++CIUDDARxXR2O0TP5mYKvgb5mFHMe25Q4VlPT7R5AwYKDbz0xxrqii56BtSrNlaq/Gi954i0Dr+4b4xeD; ssxmod_itna2=QqGxnDgDcA0=G=G7DhPHI5ijY7j5DvKDXDUqAjQGgDYq7=GFDmx0P8pa2AKq+K+xe2e+0GA7=+o4DW+KnirU7q+D7pYeYAG8jYr/BPxD/YicDcxq4VRCeuAaNGSvuEoTt++YwEbKA8e2ZRauPrQKehT2AFhyPwFKAAG3eHH8=GxdzcOUPEF27PYhP7aXZ+4s3uIfZiqW69O189LHfIhlrH6yIHUmKOeNB8QDTMdxfD46zcqdKBTB/+eUFPKfZ2CZEy8mx6f49fENHPOhS6n0Fd0EblC4zt+sID4RZ2RGVbLTE9hU9DEE1sSlRvYFHiaQRRuKDMjFynmQm52mvQCuVt70BWUUHqp90fY5ac9BbObTGeRg9Kztwz9K0B2znBDFF3PWa/iF4u2mwknw6Q0CAP/jex4wP94PqTQmHQ/E+3fWtybdqTPasI3imTX4q0Bbs0nBC+a3ndwwTepgzwFim3oSOS778PZFdO6cDWnDsGpfT7v95iS6R50S+MA44IwdkHxNHM4+OQmz8Q//5pi7qeunKA+UuWTPOtCaGvzm5euFaWk/DHhWCaG784l0Wmv9orhjM7q/jM0t8f=gkf+plcsa0fUPcz2cFd=NMi=UL07M3IWhT0A4Lnyndkfbp=u7FqE+qWCtmnk5m8R4G+GaMalxatKrkmwYlq/mH9aSP+Fi0l64x8S1j0Cie2hwnDeaExGeIxe5ZuMOP4xklqsbz0DKAq8dH2Wi1ZaxjPQiOBQP4mCY4HKSYN+u0G84Ni3YG8ODv+0o7LBOn+2xLY4ZHxhDY0iZqtDra7ePz=KTbN/+2BSOGB27nKP7HlDzPwiWaIxIOHhpaiaoT/dwxZiWZahnesGrmqgikmqMiNnqdaqlx4rORq+D4Y4wieYDD",
                "elastic-apm-traceparent": "00-1b9182260ba3be8e2fccd60500ee2795-14c77ad6d9497e7a-00",
                "host": "xueqiu.com",
                "pragma": "no-cache",
                "referer": "https://xueqiu.com/S/01810?md5__1038=n4%2BxRD9iDQ0Q0%3DG8QGCDl6jm5GIcuh%2BGShfrTD",
                "sec-ch-ua": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
                "x-requested-with": "XMLHttpRequest"
            }
            url =f'{url}&md5__1038={self.md5(url)}'
            response = requests.get(url, headers=headers2)
            print(url)
            if response.status_code == 200:
                #print(response.text)
                t_json=json.loads(response.text)
                #print(t_json['msg'])
                count=math.ceil(t_json['count'] / 10)
                last_id = self.json_get(t_json)

            time.sleep(random.randint(1, 5))

if __name__ == "__main__":
    a=XueQiu()
    i=0
    with open('C:/Users/0/Desktop/studio/Synthetic-DSS/a/股票代码.json', 'r', encoding='utf-8') as file:
    # 读取文件内容并解析为 Python 对象
        datas = json.load(file)
    for data in datas['XueQiu']:
        a.search_articles('SZ000001')
        i=i+1
        break
        print(i)
        
