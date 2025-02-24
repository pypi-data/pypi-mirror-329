import time
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.qube_ab19facb92 import EngineBuilder
from project.logger_config import logger
class MysqlConnector(EngineBuilder):
	def __init__(A,host,port,user,password,database):super().__init__(host=host,port=port,user=user,password=password,database=database,engine_name='mysql');A.connector=A.build_mysql()
	def test_connection(A):
		B=False
		try:
			if A.connector.is_connected():A.connector.close();return True
			else:return B
		except Exception as C:logger.debug(f"Error: {C}");return B