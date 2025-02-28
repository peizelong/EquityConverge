#from CrawlingModule import MongoDB
from pymongo import MongoClient
import XueQiu
import re
import datetime
#a= MongoDB.MongoDBHelper()



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


def check_strings_with_keywords(text, fixed_keyword, other_keywords,url):
    """
    检查文本按 \n 分割后的每个字符串是否包含固定关键词或其他关键词中的任意一个
    :param text: 待检查的文本，以 \n 作为分隔符
    :param fixed_keyword: 固定关键词
    :param other_keywords: 多个关键词组成的列表
    :return: 符合条件的字符串列表
    """
    # 将文本按 \n 分割成字符串列表
    strings = text.split('\n')
    result = []
    for string in strings:
        # 检查是否包含固定关键词或其他关键词中的任意一个
        if fixed_keyword in string and any(keyword in string for keyword in other_keywords):
            #result.append(string)
            write_text_to_file(f'{string}[[链接]]({url})','C:/Users/0/Desktop/studio/InformationSystem/b.md')
    return result

def check(datas,keyword,result):
    is_key_in_title = False
    if keyword in result['标题']:
        is_key_in_title = True
    a = result['内容'].count(keyword)
    if is_key_in_title :
        a=a+1
    if a > 3:
        dt_object = datetime.datetime.strptime(result['时间'], "%Y-%m-%d %H:%M:%S")

        # 将 datetime 对象转换为秒级时间戳
        timestamp_seconds = dt_object.timestamp()

        # 将秒级时间戳转换为毫秒级时间戳
        timestamp_milliseconds = int(timestamp_seconds * 1000)
        item = {
                "标题": result['标题'],
                "url": f'https://www.jiuyangongshe.com/a/{result['ID']}',
                "时间": timestamp_milliseconds,
                "内容": result['内容']
        }
        datas.append(item)
    return datas
        #write_text_to_file(f'## {result['标题']}  {result['时间']}\n',f'{fixed_keyword}.md')
        #write_text_to_file(f'{result['内容']}\n',f'{fixed_keyword}.md')
# 雪球
def check2(datas,keyword,result):
    is_key_in_title = False
    if keyword in result['title']:
        is_key_in_title = True
    a = result['text'].count(keyword)
    if is_key_in_title :
        a=a+1
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

def getText(fixed_keyword,keyID):
    # 公司关键词


    datas = []

    xueqiu = XueQiu.XueQiu()
    # 连接到 MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    # 选择数据库
    db = client['InformationSystem']
    # 选择集合
    collection = db['JiuYan']
    collection2 = db['XueQiu']

    # 构建正则表达式
    fixed_pattern = re.compile(fixed_keyword, re.IGNORECASE)


    # 构建查询条件
    query = {
        '$or': [
            {'title': {'$regex': fixed_keyword, '$options': 'i'}},
            {'text': {'$regex': fixed_keyword, '$options': 'i'}}
        ]
    }
    #雪球
    query2 = {
        '$or': [
            {'title': {'$regex': fixed_keyword, '$options': 'i'}},
            {'text': {'$regex': fixed_keyword, '$options': 'i'}}
        ]
    }
    # 执行查询
    results = collection.find(query)
    xueqiu.search_articles(keyID)
    results2 = collection2.find(query2)

    # 输出查询结果
    for result in results:
        #print(result)
        check(datas,fixed_keyword,result)
        #print(a)
    for result in results2:
        #print(result)
        check2(datas,fixed_keyword,result)
        #print(a)
    # 关闭连接
    sorted_datas = sorted(datas, key=lambda x: x["时间"], reverse=True)
    text=''
    for data in sorted_datas:
            dt_object = datetime.datetime.fromtimestamp(data['时间']/1000)

            # 将 datetime 对象格式化为日期字符串
            date_string = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            write_text_to_file(f'## [{data['标题']}  {date_string}]({data['url']})\n',f'{fixed_keyword}.md')
            write_text_to_file(f'{data['内容']}\n',f'{fixed_keyword}.md')
            #print("-------------------------")
    client.close()

getText('中金公司','SH601995')