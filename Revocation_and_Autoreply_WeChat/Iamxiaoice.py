# -*-encoding:utf-8 -*-
import itchat
from itchat.content import *
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')   

global name #用来记录消息的发送者

# 记录消息发送者的username，然后把消息发送给微软小冰
# 注册器：Text，Map，Card，Note，Sharing
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], True, False, False)
def sendTextToXiaoice(msg):
    global name
    name = msg['FromUserName']
    itchat.send(msg['Text'], toUserName='@1fa142a3e1bb31a0d8ec6d157b704485') #不知小冰用不了wechatid=‘xiaoice-ms’，但是文件传输助手filehelper可以用，所以这里利用小冰的username

# 记录消息发送者的username，然后把消息发送给微软小冰
# 注册器：Picture，Recording，Attachment，Video
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], True, False, False)
def sendToXiaoice(msg):
    global name
    name = msg['FromUserName']
    msg['Text'](msg['FileName'])
    itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']), toUserName='@1fa142a3e1bb31a0d8ec6d157b704485')

# 将小冰回复的消息发给发送者
# 注册器：Text，Map，Card，Note，Sharing
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], False, False, True)
def replyTextToSender(msg):
    global name
    itchat.send(msg['Text'], name)

# 将小冰回复的消息（图片等）发给发送者
# 注册器：Picture，Recording，Attachment，Video
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], False, False, True)
def replyToSender(msg):
    global name
    msg['Text'](msg['FileName'])
    itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']), name)

itchat.auto_login(hotReload=True)
itchat.run()
