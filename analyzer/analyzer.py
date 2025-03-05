import datetime
import time
import pymongo
import pandas as pd


def get_timestamp_range(date_str):
    """
    根据输入的日期字符串获取该天的时间戳范围
    :param date_str: 日期字符串，格式为 'YYYY-MM-DD'
    :return: 包含该天起始时间戳和结束时间戳的元组
    """
    try:
        # 将日期字符串转换为 date 对象
        target_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

        # 计算该天零点的时间
        start_of_day = datetime.datetime.combine(target_date, datetime.time.min)

        # 计算该天 23:59:59.999999 的时间
        end_of_day = datetime.datetime.combine(target_date, datetime.time.max)

        # 将 datetime 对象转换为时间戳
        start_timestamp = time.mktime(start_of_day.timetuple())
        end_timestamp = time.mktime(end_of_day.timetuple()) + end_of_day.microsecond / 1e6

        return start_timestamp*1000, end_timestamp*1000
    except ValueError:
        print("输入的日期格式不正确，请使用 'YYYY-MM-DD' 格式。")
        return None

def get_hot(symbol,keyword):
    score = 0
    query = {
        "tag": symbol,
        "time": {
            "$gte": start_timestamp,
            "$lte": end_timestamp
        }
    }
    # 执行查询
    results = collection.find(query)
    # 输出结果


    for result in results:
        is_key_in_title = False
        if keyword in result['title']:
            is_key_in_title = True
        count = result['text'].count(keyword)
        if is_key_in_title :
            score=score+2
        if count >= 2:
            score = score +1
    # 关闭连接

    return score

 
# 示例使用

excel_file=pd.ExcelFile('res/hot.xlsx')

df = excel_file.parse('LunTan')


client = pymongo.MongoClient('mongodb://localhost:27017/')
# 选择数据库
db = client['ECSystem']
# 选择集合
collection = db['XueQiu']

start_timestamp,end_timestamp = get_timestamp_range('2025-03-02')



hot_tab=[]
for row in df.itertuples():
    #print(row.Index)
    a= get_hot(symbol=row[1],keyword=row[2])
    print(a)
    hot_tab.append(a)
df["2025-03-02"]=hot_tab
with pd.ExcelWriter('res/hot.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='LunTan', index=False)


