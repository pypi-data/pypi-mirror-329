_A=False
import os,duckdb,pandas as pd
from project.sparta_662ef67a08.sparta_69edb439b9.qube_365975f128 import EngineBuilder
from project.logger_config import logger
class DuckDBConnector(EngineBuilder):
	def __init__(A,database_path,read_only=_A):B=database_path;super().__init__(host=None,port=None,database=B);A.connector=A.build_duckdb(database_path=B,read_only=read_only)
	def test_connection(A):
		if A.database is None:A.error_msg_test_connection='Empty database path';return _A
		if not os.path.exists(A.database)and A.database!=':memory:':A.error_msg_test_connection='Invalid database path';return _A
		try:A.connector.execute('SELECT 1');A.connector.close();return True
		except Exception as B:A.error_msg_test_connection=str(B);return _A
	def get_available_tables(A):
		try:B=A.connector.execute('SHOW TABLES').fetchall();A.connector.close();C=[A[0]for A in B];return C
		except Exception as D:A.connector.close();logger.debug(f"Failed to list tables: {D}");return[]
	def get_table_columns(A,table_name):
		B=table_name
		try:C=f"PRAGMA table_info('{B}')";D=A.connector.execute(C).fetchall();A.connector.close();E=[A[1]for A in D];return E
		except Exception as F:A.connector.close();logger.debug(f"Failed to list columns for table '{B}': {F}");return[]
	def get_data_table(A,table_name):
		try:B=f"SELECT * FROM {table_name}";C=A.connector.execute(B).df();A.connector.close();return C
		except Exception as D:A.connector.close();raise Exception(D)