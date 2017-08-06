#Based on module -- itchat
#Based on zhihu:https://zhuanlan.zhihu.com/p/25689314
#Author:linjiafengyang


# -*-encoding:utf-8-*-
import re
import os
import shutil
import time
import itchat
from itchat.content import *

# {msg_id:(msg_from,msg_to,msg_time,msg_time_touser,msg_type,msg_content,msg_url)}
msg_dict = {}

#将接收到的消息存入字典中，当接收到新消息时对字典中超时的消息清理
#不需要注册note(通知类)消息，通知类消息一般为红包、转账、消息撤回提醒等，不具备撤回功能
@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO, FRIENDS])
def Revocation(msg):
    #本地时间
    myTime = time.localtime()
    #获取用于展示给用户看的时间2017/08/03 18:12:20
    msg_time_touser = myTime.tm_year.__str__() \
                        + "/" + myTime.tm_mon.__str__() \
                        + "/" + myTime.tm_mday.__str__() \
                        + " " + myTime.tm_hour.__str__() \
                        + ":" + myTime.tm_min.__str__() \
                        + ":" + myTime.tm_sec.__str__()
    msg_id = msg['MsgId'] #消息ID
    msg_time = msg['CreateTime'] #消息时间
    #消息发送者昵称
    msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']
    msg_type = msg['Type'] #消息类型
    msg_content = None #消息内容
    msg_url = None #分享类消息有url
    #图片 语音 附件 视频，可下载消息将内容下载暂存到当前目录
    if msg['Type'] == 'Text':
        msg_content = msg['Text']
    elif msg['Type'] == 'Picture':
        msg_content = msg['FileName']
        msg['Text'](msg['FileName'])
    elif msg['Type'] == 'Card':
        msg_content = msg['RecommendInfo']['NickName'] + r" 的名片"
    elif msg['Type'] == 'Map':
        x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1,2,3)
        if location is None:
            msg_content = r"位置：纬度->" + x.__str__() + "经度->" + y.__str__()
        else:
            msg_content = r"位置：" + location
    elif msg['Type'] == 'Sharing':
        msg_content = msg['Text']
        msg_url = msg['Url']
    elif msg['Type'] == 'Recording':
        msg_content = msg['FileName']
        msg['Text'](msg['FileName'])
    elif msg['Type'] == 'Attachment':
        msg_content = r"文件：" + msg['FileName']
        msg['Text'](msg['FileName'])
    elif msg['Type'] == 'Video':
        msg_content = r"视频：" + msg['FileName']
        msg['Text'](msg['FileName'])
    elif msg['Type'] == 'Friends':
        msg_content = msg['Text']
    #无需自动回复可将这一行注释掉
    itchat.send(r"【自动回复】已收到你在【%s】发送的信息【%s】。我现在有事不在，稍后回复。" % (msg_time_touser, msg_content), toUserName=msg['FromUserName'])
    msg_dict.update(
        {
            msg_id: {
                "msg_from": msg_from,
                "msg_time": msg_time,
                "msg_time_touser": msg_time_touser,
                'msg_type': msg_type,
                "msg_content": msg_content,
                "msg_url": msg_url
            }
        }
    )
    clearTimeOutMsg()

#note类消息，这里主要利用撤回的note类消息，在电脑端当前文件夹创建revocation文件夹，用来保存图片，语音，视频，附件等可下载消息
@itchat.msg_register([NOTE])
def SaveMsg(msg):
    #创建存放可下载信息内容的文件夹
    if not os.path.exists(".\\revocation\\"):
        os.mkdir(".\\revocation\\")
    #看看msg里面究竟是什么
    print (msg)
    if re.search(r"\<replacemsg\>\<\!\[CDATA\[.*撤回了一条消息\]\]\>\<\/replacemsg\>", msg['Content']) != None:
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        #print无关紧要
        print (old_msg_id)
        old_msg = msg_dict.get(old_msg_id, {})
        msg_send = r"好友：" \
                    + old_msg.get('msg_from', None) \
                    + r" 在【" + old_msg.get('msg_time_touser', None) \
                    + r"】撤回了一条【" + old_msg['msg_type'] + "】消息，内容如下：" \
                    + old_msg.get('msg_content', None)
        if old_msg['msg_type'] == "Sharing":
            msg_send += r"链接：" \
                        + old_msg.get('msg_url', None)
        elif old_msg['msg_type'] == 'Picture' \
                or old_msg['msg_type'] == 'Recording' \
                or old_msg['msg_type'] == 'Video' \
                or old_msg['msg_type'] == 'Attachment':
            msg_send += r"，存储在当前目录下revocation文件夹中"
            shutil.move(old_msg['msg_content'], r".\\revocation\\")
        itchat.send(msg_send, toUserName='filehelper')
        msg_dict.pop(old_msg_id)
        clearTimeOutMsg()
    #微信英文版撤回
    if re.search(r"\<replacemsg\>\<\!\[CDATA\[.*has recalled a message.\]\]\>\<\/replacemsg\>", msg['Content']) != None:
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        print (old_msg_id)
        old_msg = msg_dict.get(old_msg_id, {})
        msg_send = r"好友：" \
                    + old_msg.get('msg_from', None) \
                    + r" 在【" + old_msg.get('msg_time_touser', None) \
                    + r"】撤回了一条【" + old_msg['msg_type'] + "】消息，内容如下：" \
                    + old_msg.get('msg_content', None)
        if old_msg['msg_type'] == "Sharing":
            msg_send += r"链接：" \
                        + old_msg.get('msg_url', None)
        elif old_msg['msg_type'] == 'Picture' \
                or old_msg['msg_type'] == 'Recording' \
                or old_msg['msg_type'] == 'Video' \
                or old_msg['msg_type'] == 'Attachment':
            msg_send += r"，存储在当前目录下revocation文件夹中"
            shutil.move(old_msg['msg_content'], r".\\revocation\\")
        itchat.send(msg_send, toUserName='filehelper')
        msg_dict.pop(old_msg_id)
        clearTimeOutMsg()
   
#clearTimeOutMsg用于清理超时的消息（超过两分钟）
#为减少资源占用，此函数只在有新消息时调用
def clearTimeOutMsg():
    if msg_dict.__len__() > 0:
        for msgid in list(msg_dict):
            print("c:" + msgid)
            #超时2分钟
            if time.time() - msg_dict.get(msgid, None)["msg_time"] > 130.0:
                item = msg_dict.pop(msgid)
                print ("超时的消息：", item['msg_content'])
                #可下载类的消息，并删除相关文件
                if item['msg_type'] == "Picture" \
                    or item['msg_type'] == "Recording" \
                    or item['msg_type'] == "Video" \
                    or item['msg_type'] == "Attachment":
                    print ("要删除的文件：", item['msg_content'])
                    os.remove(item['msg_content'])

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()

"""
# 自动回复
# 封装好的装饰器
@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO])
def text_reply(msg):
    if msg['Type'] == 'Text':
        reply_content = msg['Text']
    elif msg['Type'] == 'Picture':
        reply_content = r"图片：" + msg['FileName']
    elif msg['Type'] == 'Card':
        reply_content = r" " + msg['RecommendInfo']['NickName'] + r" 的名片"
    elif msg['Type'] == 'Map':
        x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1,2,3)
        if location is None:
            reply_content = r"位置：纬度->" + x.__str__() + "经度->" + y.__str__()
        else:
            reply_content = r"位置：" + location
    elif msg['Type'] == 'Note':
        reply_content = r"通知"
    elif msg['Type'] == 'Sharing':
        reply_content = r"分享"
    elif msg['Type'] == 'Recording':
        reply_content = r"语音"
    elif msg['Type'] == 'Attachment':
        reply_content = r"文件：" + msg['FileName']
    elif msg['Type'] == 'Video':
        reply_content = r"视频：" + msg['FileName']
    else:
        reply_content = r"消息"

    friend = itchat.search_friends(userName=msg['FromUserName'])
    itchat.send(r"Friend:%s -- %s   "
                r"Time:%s   "
                r"Message:%s" % (friend['NickName'], friend['RemarkName'], time.ctime(), reply_content),
                toUserName='filehelper')
    itchat.send(r"【自动回复】已收到你在【%s】发送的信息【%s】，我现在有事不在，稍后回复。" % (time.ctime(), reply_content), toUserName=msg['FromUserName'])
"""

"""
#登录
#itchat.login()

#获取好友列表
#friends = itchat.get_friends(update=True)[0:]


#初始化计数器，有男有女，除此有些人不填性别，1表示男性，2女性
#排除自己，故用friends[1:]
male = female = other = 0;
for i in friends[1:]:
	sex = i["Sex"]
	if sex == 1:
		male += 1
	elif sex == 2:
		female += 1
	else:
		other += 1
#好友总数
total = len(friends[1:])

print ("男性朋友：%d, 女性朋友：%d, 其他：%d" % (male, female, other))

#好友个性签名
for i in friends:
	signature = i["Signature"]
	print (signature)
"""
