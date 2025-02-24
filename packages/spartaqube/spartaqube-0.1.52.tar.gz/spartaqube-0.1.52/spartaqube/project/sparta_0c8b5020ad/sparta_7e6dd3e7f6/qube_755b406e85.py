_H='execution_count'
_G='cell_type'
_F='code'
_E='outputs'
_D='source'
_C='cells'
_B='sqMetadata'
_A='metadata'
import os,re,uuid,json
from datetime import datetime
from nbconvert.filters import strip_ansi
from project.sparta_0c8b5020ad.sparta_a269ae17c3 import qube_e016ad5093 as qube_e016ad5093
from project.sparta_0c8b5020ad.sparta_2b5b2a60e0.qube_979597c799 import sparta_2d3e41973b,sparta_16309ca73f
from project.logger_config import logger
def sparta_25fa00b5b4(file_path):return os.path.isfile(file_path)
def sparta_048331e942():return qube_e016ad5093.sparta_93d4face8f(json.dumps({'date':str(datetime.now())}))
def sparta_8e23092494():B='python';A='name';C={'kernelspec':{'display_name':'Python 3 (ipykernel)','language':B,A:'python3'},'language_info':{'codemirror_mode':{A:'ipython','version':3},'file_extension':'.py','mimetype':'text/x-python',A:B,'nbconvert_exporter':B,'pygments_lexer':'ipython3'},_B:sparta_048331e942()};return C
def sparta_55e01d7f5f():return{_G:_F,_D:[''],_A:{},_H:None,_E:[]}
def sparta_732cc13536():return[sparta_55e01d7f5f()]
def sparta_6b79a9092f():return{'nbformat':4,'nbformat_minor':0,_A:sparta_8e23092494(),_C:[]}
def sparta_5c0448661b(first_cell_code=''):A=sparta_6b79a9092f();B=sparta_55e01d7f5f();B[_D]=[first_cell_code];A[_C]=[B];return A
def sparta_5d55803766(full_path):
	A=full_path
	if sparta_25fa00b5b4(A):return sparta_e2b37373c7(A)
	else:return sparta_5c0448661b()
def sparta_e2b37373c7(full_path):return sparta_57d896a839(full_path)
def sparta_cafa80e005():A=sparta_6b79a9092f();B=json.loads(qube_e016ad5093.sparta_648fc34e67(A[_A][_B]));A[_A][_B]=B;return A
def sparta_57d896a839(full_path):
	with open(full_path)as C:B=C.read()
	if len(B)==0:A=sparta_6b79a9092f()
	else:A=json.loads(B)
	A=sparta_4281a0c253(A);return A
def sparta_4281a0c253(ipynb_dict):
	A=ipynb_dict;C=list(A.keys())
	if _C in C:
		D=A[_C]
		for B in D:
			if _A in list(B.keys()):
				if _B in B[_A]:B[_A][_B]=qube_e016ad5093.sparta_648fc34e67(B[_A][_B])
	try:A[_A][_B]=json.loads(qube_e016ad5093.sparta_648fc34e67(A[_A][_B]))
	except:A[_A][_B]=json.loads(qube_e016ad5093.sparta_648fc34e67(sparta_048331e942()))
	return A
def sparta_658012335a(full_path):
	B=full_path;A=dict()
	with open(B)as C:A=C.read()
	if len(A)==0:A=sparta_cafa80e005();A[_A][_B]=json.dumps(A[_A][_B])
	else:
		A=json.loads(A)
		if _A in list(A.keys()):
			if _B in list(A[_A].keys()):A=sparta_4281a0c253(A);A[_A][_B]=json.dumps(A[_A][_B])
	A['fullPath']=B;return A
def save_ipnyb_from_notebook_cells(notebook_cells_arr,full_path,dashboard_id='-1'):
	R='output_type';Q='markdown';L=full_path;K='tmp_idx';B=[]
	for A in notebook_cells_arr:
		A['bIsComputing']=False;S=A['bDelete'];F=A['cellType'];M=A[_F];T=A['positionIndex'];A[_D]=[M];G=A.get('ipynbOutput',[]);C=A.get('ipynbError',[]);logger.debug('ipynb_output_list');logger.debug(G);logger.debug(type(G));logger.debug('ipynb_error_list');logger.debug(C);logger.debug(type(C));logger.debug('this_cell_dict');logger.debug(A)
		if int(S)==0:
			if F==0:H=_F
			elif F==1:H=Q
			elif F==2:H=Q
			elif F==3:H='raw'
			D={_A:{_B:qube_e016ad5093.sparta_93d4face8f(json.dumps(A))},'id':uuid.uuid4().hex[:8],_G:H,_D:[M],_H:None,K:T,_E:[]}
			if len(G)>0:
				N=[]
				for E in G:O={};O[E['type']]=[E['output']];N.append({'data':O,R:'execute_result'})
				D[_E]=N
			elif len(C)>0:
				D[_E]=C
				try:
					J=[];U=re.compile('<ipython-input-\\d+-[0-9a-f]+>')
					for E in C:E[R]='error';J+=[re.sub(U,'<IPY-INPUT>',strip_ansi(A))for A in E['traceback']]
					if len(J)>0:D['tbErrors']='\n'.join(J)
				except Exception as V:logger.debug('Except prepare error output traceback with msg:');logger.debug(V)
			else:D[_E]=[]
			B.append(D)
	B=sorted(B,key=lambda d:d[K]);[A.pop(K,None)for A in B];I=sparta_5d55803766(L);P=I[_A][_B];P['identifier']={'dashboardId':dashboard_id};I[_A][_B]=qube_e016ad5093.sparta_93d4face8f(json.dumps(P));I[_C]=B
	with open(L,'w')as W:json.dump(I,W,indent=4)
	return{'res':1}
def sparta_d33b4b9bc7(full_path):
	A=full_path;A=sparta_2d3e41973b(A);C=dict()
	with open(A)as D:E=D.read();C=json.loads(E)
	F=C[_C];B=[]
	for G in F:B.append({_F:G[_D][0]})
	logger.debug('notebook_cells_list');logger.debug(B);return B