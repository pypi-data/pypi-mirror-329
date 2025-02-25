_C='json_api'
_B='postgres'
_A=None
import time,json,pandas as pd
from pandas.api.extensions import no_default
import project.sparta_662ef67a08.sparta_69edb439b9.qube_71ecad3bbe as qube_71ecad3bbe
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_7b222aa485.qube_59e6829e85 import AerospikeConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_a01deb1b97.qube_53eaef1be6 import CassandraConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_abc930f26d.qube_3fa7fa3f1e import ClickhouseConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_72dca6a4ae.qube_45e925fae5 import CouchdbConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_6c4c37ec51.qube_b5d4d70bdd import CsvConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_3b644377a2.qube_5ff243f95e import DuckDBConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_b07afdccc9.qube_aa5aac3d38 import JsonApiConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_3bc27da6c5.qube_7c618af000 import InfluxdbConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_742c834a07.qube_9e4ec25db8 import MariadbConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_ae4fb0af30.qube_d76c88ce88 import MongoConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_87a84fc032.qube_66dbf17e43 import MssqlConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_a217831a7d.qube_5ee6f311c7 import MysqlConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_cc7bfe5790.qube_d0f4094bb7 import OracleConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_20502ec6c3.qube_ea1ccba009 import ParquetConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_aea40d8f89.qube_6b2fa6c605 import PostgresConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_e24f9dd1c1.qube_582f53ef19 import PythonConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_ecaa5715ea.qube_585632d1dd import QuestDBConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_670805b894.qube_e770af4830 import RedisConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_424abf6ae1.qube_c6b8f425ad import ScylladbConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_7a6f6dab54.qube_e8ef3b68d2 import SqliteConnector
from project.sparta_662ef67a08.sparta_69edb439b9.sparta_07de0ba330.qube_be6518307b import WssConnector
from project.logger_config import logger
class Connector:
	def __init__(A,db_engine=_B):A.db_engine=db_engine
	def init_with_model(B,connector_obj):
		A=connector_obj;E=A.host;F=A.port;G=A.user;H=A.password_e
		try:C=qube_71ecad3bbe.sparta_dd736bc64f(H)
		except:C=_A
		I=A.database;J=A.oracle_service_name;K=A.keyspace;L=A.library_arctic;M=A.database_path;N=A.read_only;O=A.json_url;P=A.socket_url;Q=A.db_engine;R=A.csv_path;S=A.csv_delimiter;T=A.token;U=A.organization;V=A.lib_dir;W=A.driver;X=A.trusted_connection;D=[]
		if A.dynamic_inputs is not _A:
			try:D=json.loads(A.dynamic_inputs)
			except:pass
		Y=A.py_code_processing;B.db_engine=Q;B.init_with_params(host=E,port=F,user=G,password=C,database=I,oracle_service_name=J,csv_path=R,csv_delimiter=S,keyspace=K,library_arctic=L,database_path=M,read_only=N,json_url=O,socket_url=P,dynamic_inputs=D,py_code_processing=Y,token=T,organization=U,lib_dir=V,driver=W,trusted_connection=X)
	def init_with_params(A,host,port,user=_A,password=_A,database=_A,oracle_service_name='orcl',csv_path=_A,csv_delimiter=_A,keyspace=_A,library_arctic=_A,database_path=_A,read_only=False,json_url=_A,socket_url=_A,redis_db=0,token=_A,organization=_A,lib_dir=_A,driver=_A,trusted_connection=True,dynamic_inputs=_A,py_code_processing=_A):
		J=keyspace;I=py_code_processing;H=dynamic_inputs;G=database_path;F=database;E=password;D=user;C=port;B=host
		if A.db_engine=='aerospike':A.db_connector=AerospikeConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='cassandra':A.db_connector=CassandraConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='clickhouse':A.db_connector=ClickhouseConnector(host=B,port=C,database=F,user=D,password=E)
		if A.db_engine=='couchdb':A.db_connector=CouchdbConnector(host=B,port=C,user=D,password=E)
		if A.db_engine=='csv':A.db_connector=CsvConnector(csv_path=csv_path,csv_delimiter=csv_delimiter)
		if A.db_engine=='duckdb':A.db_connector=DuckDBConnector(database_path=G,read_only=read_only)
		if A.db_engine=='influxdb':A.db_connector=InfluxdbConnector(host=B,port=C,token=token,organization=organization,bucket=F,user=D,password=E)
		if A.db_engine==_C:A.db_connector=JsonApiConnector(json_url=json_url,dynamic_inputs=H,py_code_processing=I)
		if A.db_engine=='mariadb':A.db_connector=MariadbConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mongo':A.db_connector=MongoConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mssql':A.db_connector=MssqlConnector(host=B,port=C,trusted_connection=trusted_connection,driver=driver,user=D,password=E,database=F)
		if A.db_engine=='mysql':A.db_connector=MysqlConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='oracle':A.db_connector=OracleConnector(host=B,port=C,user=D,password=E,database=F,lib_dir=lib_dir,oracle_service_name=oracle_service_name)
		if A.db_engine=='parquet':A.db_connector=ParquetConnector(database_path=G)
		if A.db_engine==_B:A.db_connector=PostgresConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='python':A.db_connector=PythonConnector(py_code_processing=I,dynamic_inputs=H)
		if A.db_engine=='questdb':A.db_connector=QuestDBConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='redis':A.db_connector=RedisConnector(host=B,port=C,user=D,password=E,db=redis_db)
		if A.db_engine=='scylladb':A.db_connector=ScylladbConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='sqlite':A.db_connector=SqliteConnector(database_path=G)
		if A.db_engine=='wss':A.db_connector=WssConnector(socket_url=socket_url,dynamic_inputs=H,py_code_processing=I)
	def get_db_connector(A):return A.db_connector
	def test_connection(A):return A.db_connector.test_connection()
	def sparta_b1a9dd415f(A):return A.db_connector.preview_output_connector()
	def get_error_msg_test_connection(A):return A.db_connector.get_error_msg_test_connection()
	def get_available_tables(A):B=A.db_connector.get_available_tables();return B
	def get_table_columns(A,table_name):B=A.db_connector.get_table_columns(table_name);return B
	def get_data_table(A,table_name):
		if A.db_engine==_C:return A.db_connector.get_json_api_dataframe()
		else:B=A.db_connector.get_data_table(table_name);return pd.DataFrame(B)
	def get_data_table_query(A,sql,table_name=_A):return A.db_connector.get_data_table_query(sql,table_name=table_name)