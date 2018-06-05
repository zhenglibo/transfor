#! /usr/bin/env python3
import sys
import pymysql
Impedance_Num = [1,2,3]
Impedance_Real = [11111,22222,12121]
Impedance_Imag = [21212,3232,4343]
def UpdateSql():
	i = 0
	dbconn = pymysql.connect("123.206.178.103","root","040912240sc","ImpedanceInfo",charset = 'utf8')
	Cursor = dbconn.cursor()
	Bufsize = 3
	while i < Bufsize:
		Sql = "INSERT INTO impedance_value(Impedance_Real,Impedance_Imag)VALUES\
		(%d,%d)"%(Impedance_Real[i],Impedance_Imag[i])
		try:
			Cursor.execute(Sql)
			dbconn.commit()
		except:
			dbconn.rollback()
			print("insert failure")
		i = i + 1
	dbconn.close()
if __name__ == '__main__':
	UpdateSql()
	sys.exit()
