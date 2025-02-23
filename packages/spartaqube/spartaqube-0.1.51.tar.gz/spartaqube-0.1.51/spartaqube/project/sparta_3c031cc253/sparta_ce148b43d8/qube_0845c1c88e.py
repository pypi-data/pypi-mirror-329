import os
from project.sparta_3c031cc253.sparta_ce148b43d8.qube_a08759c893 import qube_a08759c893
from project.sparta_3c031cc253.sparta_ce148b43d8.qube_5eb3a6a3b6 import qube_5eb3a6a3b6
from project.sparta_3c031cc253.sparta_ce148b43d8.qube_12e327ad57 import qube_12e327ad57
from project.sparta_3c031cc253.sparta_ce148b43d8.qube_e7dcffae5c import qube_e7dcffae5c
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_a08759c893()
		elif A.dbType==1:A.dbCon=qube_5eb3a6a3b6()
		elif A.dbType==2:A.dbCon=qube_12e327ad57()
		elif A.dbType==4:A.dbCon=qube_e7dcffae5c()
		return A.dbCon