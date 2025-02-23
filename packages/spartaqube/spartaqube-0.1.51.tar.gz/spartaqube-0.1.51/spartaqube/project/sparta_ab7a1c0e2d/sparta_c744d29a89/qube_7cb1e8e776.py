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
from project.sparta_ab7a1c0e2d.sparta_e36055a0d0 import qube_1f97513fb5 as qube_1f97513fb5
from project.sparta_ab7a1c0e2d.sparta_4fc6cad494.qube_01c35b57ea import sparta_8318efc52a,sparta_f4bb722ba1
def sparta_da0f3ca09e(file_path):return os.path.isfile(file_path)
def sparta_b56a3e2f23():return qube_1f97513fb5.sparta_e4f91ce1fc(json.dumps({'date':str(datetime.now())}))
def sparta_57aa3ff3f6():B='python';A='name';C={'kernelspec':{'display_name':'Python 3 (ipykernel)','language':B,A:'python3'},'language_info':{'codemirror_mode':{A:'ipython','version':3},'file_extension':'.py','mimetype':'text/x-python',A:B,'nbconvert_exporter':B,'pygments_lexer':'ipython3'},_B:sparta_b56a3e2f23()};return C
def sparta_8b301561fc():return{_G:_F,_D:[''],_A:{},_H:None,_E:[]}
def sparta_303e66d518():return[sparta_8b301561fc()]
def sparta_7dd8c9ac8d():return{'nbformat':4,'nbformat_minor':0,_A:sparta_57aa3ff3f6(),_C:[]}
def sparta_05024c3ff3(first_cell_code=''):A=sparta_7dd8c9ac8d();B=sparta_8b301561fc();B[_D]=[first_cell_code];A[_C]=[B];return A
def sparta_191ab6c255(full_path):
	A=full_path
	if sparta_da0f3ca09e(A):return sparta_fffef67b32(A)
	else:return sparta_05024c3ff3()
def sparta_fffef67b32(full_path):return sparta_8c6c30f1f6(full_path)
def sparta_d68abe5aa3():A=sparta_7dd8c9ac8d();B=json.loads(qube_1f97513fb5.sparta_386ccf6842(A[_A][_B]));A[_A][_B]=B;return A
def sparta_8c6c30f1f6(full_path):
	with open(full_path)as C:B=C.read()
	if len(B)==0:A=sparta_7dd8c9ac8d()
	else:A=json.loads(B)
	A=sparta_df5766ef53(A);return A
def sparta_df5766ef53(ipynb_dict):
	A=ipynb_dict;C=list(A.keys())
	if _C in C:
		D=A[_C]
		for B in D:
			if _A in list(B.keys()):
				if _B in B[_A]:B[_A][_B]=qube_1f97513fb5.sparta_386ccf6842(B[_A][_B])
	try:A[_A][_B]=json.loads(qube_1f97513fb5.sparta_386ccf6842(A[_A][_B]))
	except:A[_A][_B]=json.loads(qube_1f97513fb5.sparta_386ccf6842(sparta_b56a3e2f23()))
	return A
def sparta_8252a801ee(full_path):
	B=full_path;A=dict()
	with open(B)as C:A=C.read()
	if len(A)==0:A=sparta_d68abe5aa3();A[_A][_B]=json.dumps(A[_A][_B])
	else:
		A=json.loads(A)
		if _A in list(A.keys()):
			if _B in list(A[_A].keys()):A=sparta_df5766ef53(A);A[_A][_B]=json.dumps(A[_A][_B])
	A['fullPath']=B;return A
def save_ipnyb_from_notebook_cells(notebook_cells_arr,full_path,dashboard_id='-1'):
	R='output_type';Q='markdown';L=full_path;K='tmp_idx';B=[]
	for A in notebook_cells_arr:
		A['bIsComputing']=False;S=A['bDelete'];F=A['cellType'];M=A[_F];T=A['positionIndex'];A[_D]=[M];G=A.get('ipynbOutput',[]);C=A.get('ipynbError',[]);print('ipynb_output_list');print(G);print(type(G));print('ipynb_error_list');print(C);print(type(C));print('this_cell_dict');print(A)
		if int(S)==0:
			if F==0:H=_F
			elif F==1:H=Q
			elif F==2:H=Q
			elif F==3:H='raw'
			D={_A:{_B:qube_1f97513fb5.sparta_e4f91ce1fc(json.dumps(A))},'id':uuid.uuid4().hex[:8],_G:H,_D:[M],_H:None,K:T,_E:[]}
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
				except Exception as V:print('Except prepare error output traceback with msg:');print(V)
			else:D[_E]=[]
			B.append(D)
	B=sorted(B,key=lambda d:d[K]);[A.pop(K,None)for A in B];I=sparta_191ab6c255(L);P=I[_A][_B];P['identifier']={'dashboardId':dashboard_id};I[_A][_B]=qube_1f97513fb5.sparta_e4f91ce1fc(json.dumps(P));I[_C]=B
	with open(L,'w')as W:json.dump(I,W,indent=4)
	return{'res':1}
def sparta_c8e2c6b6e5(full_path):
	A=full_path;A=sparta_8318efc52a(A);C=dict()
	with open(A)as D:E=D.read();C=json.loads(E)
	F=C[_C];B=[]
	for G in F:B.append({_F:G[_D][0]})
	print('notebook_cells_list');print(B);return B