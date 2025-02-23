_C='json_api'
_B='postgres'
_A=None
import time,json,pandas as pd
from pandas.api.extensions import no_default
import project.sparta_ab7a1c0e2d.sparta_bb21f59158.qube_a879ba9993 as qube_a879ba9993
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_2ab68ea993.qube_d50ed53821 import AerospikeConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_adbd3f691b.qube_73467eaac1 import CassandraConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_18d0947528.qube_aa214ced9f import ClickhouseConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_3fdf54a84c.qube_03c057d378 import CouchdbConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_bd20ae3068.qube_c1ac65e99b import CsvConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_44b769d478.qube_036d9510cd import DuckDBConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_239e46c83d.qube_033b21a8d8 import JsonApiConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_d5368a2789.qube_8677166454 import InfluxdbConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_e2a79bedc0.qube_4dcc178a38 import MariadbConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_a0addd4efa.qube_4c222dcb34 import MongoConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_79e299f107.qube_d1f8524512 import MssqlConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_b0bbd4b9fa.qube_2790db1414 import MysqlConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_3ac1d1e548.qube_0c6941b991 import OracleConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_8c4382d72a.qube_36e36f9b14 import ParquetConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_088e7b5be1.qube_a378f1ea22 import PostgresConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_cf03a44636.qube_ec814a06eb import PythonConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_c9efd0d3a4.qube_b5d48328cf import QuestDBConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_fe9281db9a.qube_d5a61a0675 import RedisConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_223ea0f61f.qube_fe88341ed5 import ScylladbConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_9f7265ab25.qube_c2de958db3 import SqliteConnector
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.sparta_0be369af78.qube_b672fb2ec0 import WssConnector
class Connector:
	def __init__(A,db_engine=_B):A.db_engine=db_engine
	def init_with_model(B,connector_obj):
		A=connector_obj;E=A.host;F=A.port;G=A.user;H=A.password_e
		try:C=qube_a879ba9993.sparta_96a57a1f1f(H)
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
	def sparta_d03b64807a(A):return A.db_connector.preview_output_connector()
	def get_error_msg_test_connection(A):return A.db_connector.get_error_msg_test_connection()
	def get_available_tables(A):B=A.db_connector.get_available_tables();return B
	def get_table_columns(A,table_name):B=A.db_connector.get_table_columns(table_name);return B
	def get_data_table(A,table_name):
		if A.db_engine==_C:return A.db_connector.get_json_api_dataframe()
		else:B=A.db_connector.get_data_table(table_name);return pd.DataFrame(B)
	def get_data_table_query(A,sql,table_name=_A):return A.db_connector.get_data_table_query(sql,table_name=table_name)