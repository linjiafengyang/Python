from socket import *
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence:')
# python2.x
# message = raw_input('Input lowercase sentence:')
clientSocket.sendto(message.encode(), (serverName, serverPort))
# clientSocket.sendto(message, (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print (modifiedMessage.decode())
# print (modifiedMessage)
clientSocket.close()


# import socket

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
 
# addr = ('127.0.0.1', 10021)       #服务器端地址

# while True:
#     data = input('请输入要处理的数据:') #获得数据
#     if not data or data == 'quit':
#         break
#     s.sendto(data.encode(), addr)    #发送到服务端
#     recvdata, addr = s.recvfrom(1024)  #接收服务器端发来的数据
#     print(recvdata.decode('utf-8'))    #解码打印

# s.close()            #关闭socket