import os
from project.sparta_3500f2f8a8.sparta_7667aee07f.qube_49e8477de7 import qube_49e8477de7
from project.sparta_3500f2f8a8.sparta_7667aee07f.qube_222d43b9c7 import qube_222d43b9c7
from project.sparta_3500f2f8a8.sparta_7667aee07f.qube_384af7b96c import qube_384af7b96c
from project.sparta_3500f2f8a8.sparta_7667aee07f.qube_917581c1b2 import qube_917581c1b2
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_49e8477de7()
		elif A.dbType==1:A.dbCon=qube_222d43b9c7()
		elif A.dbType==2:A.dbCon=qube_384af7b96c()
		elif A.dbType==4:A.dbCon=qube_917581c1b2()
		return A.dbCon