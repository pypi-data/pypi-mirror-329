import os,sys,shutil,simplejson as json,datetime
from pathlib import Path
from datetime import datetime
from spartaqube_app.path_mapper_obf import sparta_638705750a
main_api=sparta_638705750a()['api']
sys.path.insert(0,main_api)
from spartaqube_utils import is_scalar,safe_to_json,rename_duplicate_columns,convert_dataframe_to_json,convert_to_dataframe,convert_to_dataframe_func
def sparta_f4bb722ba1(path):
	with open(path,'a'):os.utime(path,None)
def sparta_8318efc52a(path):A=Path(path).resolve();return str(A)
def sparta_9414855512(textOutputArr):
	A=textOutputArr
	try:A=[A for A in A if len(A)>0];A=[A for A in A if A!='Welcome to SpartaQube API'];A=[A for A in A if A!="<span style='color:#0ab70a'>You are logged</span>"];A=[A for A in A if A!='You are logged']
	except Exception as B:pass
	return A
def sparta_c82a5f4e0d(input2JsonEncode,dateFormat=None):
	C=dateFormat;import numpy as B
	class D(json.JSONEncoder):
		def default(E,obj):
			A=obj
			if isinstance(A,B.integer):return int(A)
			if isinstance(A,B.floating):return float(A)
			if isinstance(A,B.ndarray):return A.tolist()
			if isinstance(A,datetime.datetime):
				if C is not None:return A.strftime(C)
				else:return str(A)
			return super(D,E).default(A)
	A=json.dumps(input2JsonEncode,ignore_nan=True,cls=D);return A
def sparta_a6cb6d718d(path):
	A=path
	try:os.rmdir(A)
	except:
		try:os.system('rmdir /S /Q "{}"'.format(A))
		except:
			try:shutil.rmtree(A)
			except:
				try:os.remove(A)
				except:pass
def sparta_55176355eb(file_path):
	A=file_path
	try:os.remove(A);print(f"File '{A}' has been deleted.")
	except Exception as B:
		try:os.unlink(A);print(f"File '{A}' has been forcefully deleted.")
		except Exception as B:print(f"An error occurred while deleting the file: {B}")