from project.sparta_662ef67a08.sparta_69edb439b9.qube_365975f128 import EngineBuilder
from project.logger_config import logger
class PostgresConnector(EngineBuilder):
	def __init__(A,host,port,user,password,database):super().__init__(host=host,port=port,user=user,password=password,database=database,engine_name='postgresql');A.connector=A.build_postgres()
	def test_connection(A):
		B=False
		try:
			if A.connector:A.connector.close();return True
			else:return B
		except Exception as C:logger.debug(f"Error: {C}");return B