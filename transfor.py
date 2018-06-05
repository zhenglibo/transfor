#! /usr/bin/env python3
# -*- coding:utf-8 -*-
##本代码旨在不断分批接收GPRS
##模块发送来的阻抗数据
import time
import sys
import pymysql
from socket import *
from time import ctime
import re
##全局数组
AcceptNum = 6
Flag = True
##同步日志
def UpdateLogfile(DataList):
	i = 0
	Pos = len(DataList)//2
	fp = open("Logfile.txt",'a',encoding = 'UTF-8')
	fp.write("-------------------------------------------------\n")	
	string = "          日志时间:%s          \n "%(time.asctime(time.localtime(time.time()))) 
	fp.write(string)
	fp.write("-------------------------------------------------\n")
	fp.write("实部  虚部\n")
	while i < 3:
		str1 = "%d  %d\n"%(DataList[i],DataList[i+Pos])
		fp.write(str1)
		i = i+1
	fp.close()
## 同步数据库
def UpdateSql(DataList):
	i = 0
	Pos = len(DataList)//2
	dbconn = pymysql.connect("123.206.178.103","root","040912240sc",\
			"ImpedanceInfo",charset = 'utf8')
	Cursor = dbconn.cursor()
	Bufsize = AcceptNum
	while i < Bufsize/2:
		Sql = "INSERT INTO impedance_value(Impedance_Real,Impedance_Imag)VALUES(%d,%d)"%(DataList[i],DataList[i+Pos])
		try:
			Cursor.execute(Sql)
			dbconn.commit()
		except:
			dbconn.rollback()
			##打印一次即可
			if(Flag == True):
				print("Fail to Insert!")
				Flag = False
			
		i = i + 1
		Flag = True
	dbconn.close()
##字符串转换成整型
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
####监听端口
def ListenPort():
	HOST = ''
	PORT = 8080
	BufSize =1024
	StaticList = [] 
	Addr = (HOST,PORT)
	TcpSock = socket(AF_INET,SOCK_STREAM)
	TcpSock.bind(Addr)
	TcpSock.listen(10)
	print ("Listening Ports: 8080")
	while True:
		TcpAcceptSock ,Acceptaddr = TcpSock.accept()
		print ('连接成功,客户端地址为: ',Acceptaddr)
		while True:
			Data = TcpAcceptSock.recv(BufSize)
			#f分批接收数据
			StaticList += StringtoInt(Data,Data.count(b',',0,len(Data)))
			print (Data.decode())
			if len(StaticList) > AcceptNum:
				print("接收过多数据!\n")
				break
			elif len(StaticList) == AcceptNum:
				print("数据全部接收完毕!\n")
				break
			else:
				print("数据还未接收完毕,请等待...\n")
				#continue
			#msg = '{ }服务器已接收 '.format(ctime())
			msg = '{0}: The Server Accept!'.format(ctime())
			TcpAcceptSock.send(msg.encode())
			#if len(StringtoInt(Data,3)) > 3:
			#	break
			#print (StringtoInt(Data,Data.count(b',',0,len(Data)))) 	
		TcpAcceptSock.close()
		break
	TcpSock.close()
	return StaticList
#主函数
if __name__ == '__main__':
	ListData = ListenPort()
	print(ListData)
	UpdateSql(ListData[:])
	UpdateLogfile(ListData[:])
	sys.exit()	


