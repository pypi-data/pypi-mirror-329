_C='json_api'
_B='postgres'
_A=None
import time,json,pandas as pd
from pandas.api.extensions import no_default
import project.sparta_0c8b5020ad.sparta_78ee0f1ac9.qube_9f21eab4ac as qube_9f21eab4ac
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_ceaaf2a3d3.qube_f4e9dce61c import AerospikeConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_0c09eb2dd2.qube_fb8d66bbde import CassandraConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_1496e09fba.qube_4e80c9ac2a import ClickhouseConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_9f3963ce3d.qube_1766d26326 import CouchdbConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_572feffc1b.qube_5ff8ee67b5 import CsvConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_86b36bd0d7.qube_2a4f88b3ed import DuckDBConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_07c31b6ad5.qube_d89ccfa8cc import JsonApiConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_cd8d67e90e.qube_49fc67bfb4 import InfluxdbConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_5f251a6d1d.qube_6a1bcaf9f4 import MariadbConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_b88bb3653d.qube_0084d9af61 import MongoConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_38f6c79496.qube_b0d1ae7e6b import MssqlConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_5aa7ee45dc.qube_52599b161d import MysqlConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_f28858e137.qube_603d17e012 import OracleConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_1b7dad613e.qube_19c0dc19f4 import ParquetConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_cd39bcdd16.qube_1b97e1af57 import PostgresConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_ba34549066.qube_d1f4bdb08c import PythonConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_d777c0a7d2.qube_f36b107a4f import QuestDBConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_851b7966bf.qube_65f2b9423e import RedisConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_888028638a.qube_e008b617d7 import ScylladbConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_02272f6e5b.qube_c0bdfb0d42 import SqliteConnector
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.sparta_d91b58d08b.qube_dd03c2074f import WssConnector
from project.logger_config import logger
class Connector:
	def __init__(A,db_engine=_B):A.db_engine=db_engine
	def init_with_model(B,connector_obj):
		A=connector_obj;E=A.host;F=A.port;G=A.user;H=A.password_e
		try:C=qube_9f21eab4ac.sparta_62361a95fc(H)
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
	def sparta_2ee7de108f(A):return A.db_connector.preview_output_connector()
	def get_error_msg_test_connection(A):return A.db_connector.get_error_msg_test_connection()
	def get_available_tables(A):B=A.db_connector.get_available_tables();return B
	def get_table_columns(A,table_name):B=A.db_connector.get_table_columns(table_name);return B
	def get_data_table(A,table_name):
		if A.db_engine==_C:return A.db_connector.get_json_api_dataframe()
		else:B=A.db_connector.get_data_table(table_name);return pd.DataFrame(B)
	def get_data_table_query(A,sql,table_name=_A):return A.db_connector.get_data_table_query(sql,table_name=table_name)