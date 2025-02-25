import pandas as pd
from project.sparta_662ef67a08.sparta_69edb439b9.qube_365975f128 import EngineBuilder
class MssqlConnector(EngineBuilder):
	def __init__(A,host,port,trusted_connection,driver,user,password,database):super().__init__(host=host,port=port,user=user,password=password,database=database,engine_name='mssql+pyodbc');A.connector=A.build_mssql(trusted_connection,driver)
	def test_connection(B):
		C=False
		try:
			D=B.connector;A=D.cursor();F='SELECT @@VERSION';A.execute(F);E=A.fetchone()
			while E:E=A.fetchone()
			C=True
		except Exception as G:B.error_msg_test_connection=str(G)
		try:D.close()
		except:pass
		return C
	def get_available_tables(B):
		A=[]
		try:C=B.connector;D="SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'";E=pd.read_sql(D,C);A=sorted(list(E['TABLE_NAME'].values))
		except Exception as F:B.error_msg_test_connection=str(F);A=[]
		finally:C.close()
		return A
	def get_table_columns(B,table_name):
		A=[]
		try:C=B.connector;D=f"\n                SELECT COLUMN_NAME\n                FROM INFORMATION_SCHEMA.COLUMNS\n                WHERE TABLE_NAME = '{table_name}'\n                ";E=pd.read_sql(D,C);A=sorted(list(E['COLUMN_NAME'].values))
		except Exception as F:B.error_msg_test_connection=str(F);A=[]
		finally:C.close()
		return A
	def get_data_table(A,table_name):B=A.connector;C=f"SELECT * FROM {table_name}";D=pd.read_sql(C,B);return D
	def get_data_table_query(A,sql,table_name=None):B=A.connector;C=sql;D=pd.read_sql(C,B);return D