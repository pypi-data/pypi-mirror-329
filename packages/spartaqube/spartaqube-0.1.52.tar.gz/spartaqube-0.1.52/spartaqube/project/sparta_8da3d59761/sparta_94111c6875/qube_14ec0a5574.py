import os
from project.sparta_8da3d59761.sparta_94111c6875.qube_8e1caf5ca2 import qube_8e1caf5ca2
from project.sparta_8da3d59761.sparta_94111c6875.qube_51d4fb7770 import qube_51d4fb7770
from project.sparta_8da3d59761.sparta_94111c6875.qube_9a9218a6b7 import qube_9a9218a6b7
from project.sparta_8da3d59761.sparta_94111c6875.qube_0df11fce26 import qube_0df11fce26
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_8e1caf5ca2()
		elif A.dbType==1:A.dbCon=qube_51d4fb7770()
		elif A.dbType==2:A.dbCon=qube_9a9218a6b7()
		elif A.dbType==4:A.dbCon=qube_0df11fce26()
		return A.dbCon