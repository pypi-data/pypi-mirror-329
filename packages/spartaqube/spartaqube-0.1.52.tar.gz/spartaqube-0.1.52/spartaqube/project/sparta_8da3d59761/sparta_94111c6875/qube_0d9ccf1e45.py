import os
from project.sparta_8da3d59761.sparta_94111c6875.qube_51d4fb7770 import qube_51d4fb7770
from project.sparta_8da3d59761.sparta_94111c6875.qube_8e1caf5ca2 import qube_8e1caf5ca2
from project.logger_config import logger
class db_custom_connection:
	def __init__(A):A.dbCon=None;A.dbIdManager='';A.spartAppId=''
	def setSettingsSqlite(B,dbId,dbLocalPath,dbFileNameWithExtension):G='spartApp';E=dbLocalPath;C=dbId;from bqm import settings as F,settingsLocalDesktop as H;B.dbType=0;B.spartAppId=C;A={};A['id']=C;A['ENGINE']='django.db.backends.sqlite3';A['NAME']=str(E)+'/'+str(dbFileNameWithExtension);A['USER']='';A['PASSWORD']='2change';A['HOST']='';A['PORT']='';F.DATABASES[C]=A;H.DATABASES[C]=A;D=qube_8e1caf5ca2();D.setPath(E);D.setDbName(G);B.dbCon=D;B.dbIdManager=G;logger.debug(F.DATABASES)
	def getConnection(A):return A.dbCon
	def setAuthDB(A,authDB):A.dbType=authDB.dbType