# 导入
from wxauto import WeChat
import time
import getText
from JiuYan import JiuYan








is_JiuYan = True
jy_time = 0
jy=JiuYan()
# 获取微信窗口对象
wx = WeChat()
# 输出 > 初始化成功，获取到已登录窗口：xxxx

# 设置监听列表
listen_list = [
    '测试群'
]
# 循环添加监听对象
for i in listen_list:
    wx.AddListenChat(who=i, savepic=True)

# 持续监听消息，并且收到消息后回复“收到”
wait = 1  # 设置1秒查看一次是否有新消息

while True:
    #==============================
    #if is_JiuYan == True:
    #    jy_time = jy_time+1
    #if jy_time > 900:
    #    is_JiuYan = False
    #    jy_time = 0
    #    is_JiuYan = jy.New()
    #==============================
    msgs = wx.GetListenMessage()
    for chat in msgs:
        who = chat.who              # 获取聊天窗口名（人或群名）
        one_msgs = msgs.get(chat)   # 获取消息内容
        # 回复收到
        for msg in one_msgs:
            msgtype = msg.type       # 获取消息类型
            content = msg.content    # 获取消息内容，字符串类型的消息内容
            print(f'【{who}】：{content}')
        # ===================================================
        # 处理消息逻辑（如果有）
        # 
        # 处理消息内容的逻辑每个人都不同，按自己想法写就好了，这里不写了
        # 
        # ===================================================
        # 给“文件传输助手”发送文件（图片同理）
            if msgtype == 'friend':
                #chat.SendMsg('收到')  # 回复收到
                result = content.split()
                getText.getText(result[0],result[1])
                print(result[0])
                files = f'C:/Users/0/Desktop/studio/{result[0]}.md'
                
                if True!=wx.SendFiles(files, who='测试群'):
                    chat.SendMsg('暂无消息')
    time.sleep(wait)