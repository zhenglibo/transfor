#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import time
import sys
Impedance_Imag = [12222,2343,2121]
Impedance_Real = [23243,5465,37676]
def UpdateLogfile():
	i = 0
	fp = open("Logfile.txt",'a',encoding = 'UTF-8')
	fp.write("-------------------------------------------------\n")	
	string = "          日志时间:%s          \n "%(time.asctime(time.localtime(time.time()))) 
	fp.write(string)
	fp.write("-------------------------------------------------\n")
	fp.write("实部  虚部\n")
	while i < 3:
		str1 = "%d  %d\n"%(Impedance_Real[i],Impedance_Imag[i])
		fp.write(str1)
		i = i+1
	fp.close()
if __name__ == '__main__':
	UpdateLogfile()
	sys.exit()
