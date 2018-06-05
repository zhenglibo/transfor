#! /usr/bin/python3
# -*- coding:utf-8 -*-
#本代码是旨在接收分批接收数据
from socket import *
from time import ctime
import re
import sys
def StringtoInt(String,Num):
	i = 0
	List = []
	String = String.strip()
	StrList = String.split(b',')
	print(StrList)
	while i < Num:
		#StrList[i] = re.sub("\D","",StrList[i])
		List.append(int(StrList[i]))
		i= i+1
	return List

if __name__ == '__main__':
	HOST = ''
	PORT = 8080
	BufSize =1024
	StaticList = [] 
	Addr = (HOST,PORT)
	TcpSock = socket(AF_INET,SOCK_STREAM)
	TcpSock.bind(Addr)
	TcpSock.listen(10)
	print ("listen port 8080")
	while True:
		TcpAcceptSock ,Acceptaddr = TcpSock.accept()
		print ('连接成功,客户端地址为: ',Acceptaddr)
		while True:
			Data = TcpAcceptSock.recv(BufSize)
			#f分批接收数据
			StaticList.append(StringtoInt(Data,Data.count(b',',0,len(Data))))
			print (Data.decode())
			if len(StaticList) > 3:
				print("接收过多数据\n")
				break
			elif len(StaticList) == 3:
				print("数据全部接收完毕\n")
				break
			else:
				print("数据还未接收完毕,请等待..\n")
				#continue
			#msg = '{ }服务器已接收 '.format(ctime())
			msg = '{0}: the server accept '.format(ctime())
			TcpAcceptSock.send(msg.encode())
			#if len(StringtoInt(Data,3)) > 3:
			#	break
			print (StringtoInt(Data,Data.count(b',',0,len(Data)))) 	
		TcpAcceptSock.close()
		break
	TcpSock.close()
	sys.exit(0)

