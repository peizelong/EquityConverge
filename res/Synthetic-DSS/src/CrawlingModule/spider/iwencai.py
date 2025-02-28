import requests
import json
import time

url ="https://app.jiuyangongshe.com/jystock-app/api/v2/article/community"

data = {
    'is_newest': '1',
    'order': '0',
    'limit': '100',
    'start': '0',
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
    # 打印响应内容
    print(res.json())



else:
    print(f"请求失败，状态码: {res.status_code}")




