import pymongo
import time,datetime,json

from crawler import crawler

def write_text_to_file(text, file_path, mode='a', encoding='utf-8'):
    """
    将文本写入文件
    :param text: 要写入的文本内容
    :param file_path: 文件的路径
    :param mode: 文件打开模式，默认为 'w'（写入模式）
    :param encoding: 文件编码，默认为 'utf-8'
    :return: 写入成功返回 True，出现异常返回 False
    """
    try:
        with open(file_path, mode, encoding=encoding) as file:
            file.write(f'- {text}\n')
        return True
    except Exception as e:
        print(f"写入文件时出现错误: {e}")
        return False


def check2(datas,keyword,result):
    is_key_in_title = False
    if keyword in result['title']:
        is_key_in_title = True
    a = result['text'].count(keyword)
    if is_key_in_title :
        a=a+2
    if a > 3:
        #print('-----')
        item = {
            "标题": result['title'],
            "url": f'https://xueqiu.com{result['ID']}',
            "时间": result['time'],
            "内容": result['text']
        }
        datas.append(item)
    return datas
        

        # 将 datetime 对象格式化为日期字符串
        #date_string = dt_object.strftime("%Y-%m-%d %H:%M:%S")
        #write_text_to_file(f'## {result['title']}  {date_string}\n',f'{fixed_keyword}.md')
        #write_text_to_file(f'{result['text']}\n',f'{fixed_keyword}.md')


def getText(key_id):
    # 公司关键词
    fixed_keyword = ''
    with open('res/CODE.json', 'r', encoding='utf-8') as file:
        IDS = json.load(file)
    for ID in IDS:
        if ID['股票代码'][2:] == key_id:
            fixed_keyword=ID['股票简称']
    datas = []
    # 连接到 MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    # 选择数据库
    db = client['ECSystem']
    # 选择集合
    collection2 = db['XueQiu']
    #雪球
    query2 = {
        '$or': [
            {'title': {'$regex': fixed_keyword, '$options': 'i'}},
            {'text': {'$regex': fixed_keyword, '$options': 'i'}}
        ]
    }


    cra = crawler.crawler()
    cra.get_one(key_id)
    # 执行查询
    results2 = collection2.find(query2)
    # 输出查询结果
    for result in results2:
        check2(datas,fixed_keyword,result)
    # 关闭连接
    sorted_datas = sorted(datas, key=lambda x: x["时间"], reverse=True)
    text=''
    for data in sorted_datas:
        dt_object = datetime.datetime.fromtimestamp(data['时间']/1000)
        # 将 datetime 对象格式化为日期字符串
        date_string = dt_object.strftime("%Y-%m-%d %H:%M:%S")
        write_text_to_file(f'## [{data['标题']}  {date_string}]({data['url']})\n',f'{fixed_keyword}.md')
        write_text_to_file(f'{data['内容']}\n',f'{fixed_keyword}.md')
        print("-------------------------")
    client.close()

# ids= ['600141','600216','600919','600926','600941','601857','601898','603323','688208','688545','888880','000063','000938','000988,''000988','002139','002463','002698','002738','002966','002984','300415']
# for i in ids:
#     getText(i)
getText("603015")