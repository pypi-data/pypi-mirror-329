_x='stdout'
_w='makemigrations'
_v='python.exe'
_u='app.settings'
_t='DJANGO_SETTINGS_MODULE'
_s='thumbnail'
_r='static'
_q='project'
_p='previewImage'
_o='isExecCodeDisplay'
_n='isPublic'
_m='isExpose'
_l='password'
_k='lumino_layout'
_j='notebook_venv'
_i='lumino'
_h='Project not found...'
_g='You do not have the rights to access this project'
_f='models_access_examples.py'
_e='notebook_models.py'
_d='template'
_c='django_app_template'
_b='bin'
_a='Scripts'
_Z='win32'
_Y='luminoLayout'
_X='hasPassword'
_W='is_exec_code_display'
_V='is_public_notebook'
_U='main_ipynb_fullpath'
_T='has_password'
_S='is_expose_notebook'
_R='python'
_Q='description'
_P='slug'
_O='app'
_N='manage.py'
_M='notebook_id'
_L='project_path'
_K='notebook'
_J='notebook_obj'
_I='notebookId'
_H='name'
_G='main.ipynb'
_F='projectPath'
_E='errorMsg'
_D=None
_C=False
_B='res'
_A=True
import re,os,json,stat,importlib,io,sys,subprocess,platform,base64,traceback,uuid,shutil
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from spartaqube_app.path_mapper_obf import sparta_eb692a7fc2
from project.models_spartaqube import Notebook,NotebookShared
from project.models import ShareRights
from project.sparta_662ef67a08.sparta_b9c728af58 import qube_60ba9e4a49 as qube_60ba9e4a49
from project.sparta_662ef67a08.sparta_928c4c5c7e import qube_57fdffdbc8 as qube_57fdffdbc8
from project.sparta_662ef67a08.sparta_69edb439b9.qube_cd67bc8758 import Connector as Connector
from project.sparta_662ef67a08.sparta_c34a477d77 import qube_2110854333 as qube_2110854333
from project.sparta_662ef67a08.sparta_bc02ea2c9b.qube_2ac5797abc import sparta_6fbba8ac09
from project.sparta_662ef67a08.sparta_130739942b import qube_952fdf29a0 as qube_952fdf29a0
from project.sparta_662ef67a08.sparta_130739942b import qube_2025927415 as qube_2025927415
from project.sparta_662ef67a08.sparta_5e86276304.qube_90e1e70e21 import sparta_33f2973002
from project.sparta_662ef67a08.sparta_bc02ea2c9b.qube_629ebdf0bd import sparta_514ae4dea4,sparta_cc0eec96cd
from project.logger_config import logger
def sparta_19595da3d7(user_obj):
	A=qube_60ba9e4a49.sparta_88c03c9ba1(user_obj)
	if len(A)>0:B=[A.user_group for A in A]
	else:B=[]
	return B
def sparta_af7bc614fd(project_path,has_django_models=_A):
	C=has_django_models;B=project_path
	if not os.path.exists(B):os.makedirs(B)
	G=B;D=os.path.join(sparta_eb692a7fc2()[_c],_K,_d)
	for E in os.listdir(D):
		A=os.path.join(D,E);F=os.path.join(G,E)
		if os.path.isdir(A):
			H=os.path.basename(A)
			if H==_O:
				if not C:continue
			shutil.copytree(A,F,dirs_exist_ok=_A)
		else:
			I=os.path.basename(A)
			if I in[_e,_f]:
				if not C:continue
			shutil.copy2(A,F)
	return{_L:B}
def sparta_66d5bc42fc(json_data,user_obj):
	F=json_data;B=user_obj;A=F[_F];A=sparta_6fbba8ac09(A);G=Notebook.objects.filter(project_path=A).all()
	if G.count()>0:
		C=G[0];H=sparta_19595da3d7(B)
		if len(H)>0:D=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=H,notebook__is_delete=0,notebook=C)|Q(is_delete=0,user=B,notebook__is_delete=0,notebook=C))
		else:D=NotebookShared.objects.filter(is_delete=0,user=B,notebook__is_delete=0,notebook=C)
		I=_C
		if D.count()>0:
			K=D[0];J=K.share_rights
			if J.is_admin or J.has_write_rights:I=_A
		if not I:return{_B:-1,_E:'Chose another path. A project already exists at this location'}
	if not isinstance(A,str):return{_B:-1,_E:'Project path must be a string.'}
	logger.debug(_L);logger.debug(A)
	try:A=os.path.abspath(A)
	except Exception as E:return{_B:-1,_E:f"Invalid project path: {str(E)}"}
	try:
		if not os.path.exists(A):os.makedirs(A)
		L=F['hasDjangoModels'];M=sparta_af7bc614fd(A,L);A=M[_L];return{_B:1,_L:A}
	except Exception as E:return{_B:-1,_E:f"Failed to create folder: {str(E)}"}
def sparta_b961b2881a(json_data,user_obj):A=json_data;A['bAddGitignore']=_A;A['bAddReadme']=_A;return qube_2025927415.sparta_fd68c1ddb5(A,user_obj)
def sparta_df1a8065f4(json_data,user_obj):
	L='%Y-%m-%d';K='Recently used';E=user_obj;G=sparta_19595da3d7(E)
	if len(G)>0:A=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=G,notebook__is_delete=0)|Q(is_delete=0,user=E,notebook__is_delete=0)|Q(is_delete=0,notebook__is_delete=0,notebook__is_expose_notebook=_A,notebook__is_public_notebook=_A))
	else:A=NotebookShared.objects.filter(Q(is_delete=0,user=E,notebook__is_delete=0)|Q(is_delete=0,notebook__is_delete=0,notebook__is_expose_notebook=_A,notebook__is_public_notebook=_A))
	if A.count()>0:
		C=json_data.get('orderBy',K)
		if C==K:A=A.order_by('-notebook__last_date_used')
		elif C=='Date desc':A=A.order_by('-notebook__last_update')
		elif C=='Date asc':A=A.order_by('notebook__last_update')
		elif C=='Name desc':A=A.order_by('-notebook__name')
		elif C=='Name asc':A=A.order_by('notebook__name')
	H=[]
	for F in A:
		B=F.notebook;M=F.share_rights;I=_D
		try:I=str(B.last_update.strftime(L))
		except:pass
		J=_D
		try:J=str(B.date_created.strftime(L))
		except Exception as N:logger.debug(N)
		D=B.main_ipynb_fullpath
		if D is _D:D=os.path.join(B.project_path,_G)
		elif len(D)==0:D=os.path.join(B.project_path,_G)
		H.append({_M:B.notebook_id,_H:B.name,_P:B.slug,_Q:B.description,_S:B.is_expose_notebook,_T:B.has_password,_U:D,_V:B.is_public_notebook,_W:B.is_exec_code_display,'is_owner':F.is_owner,'has_write_rights':M.has_write_rights,'last_update':I,'date_created':J})
	return{_B:1,'notebook_library':H}
def sparta_c0b9d98b21(json_data,user_obj):
	C=user_obj;F=json_data[_I];E=Notebook.objects.filter(notebook_id__startswith=F,is_delete=_C).all()
	if E.count()==1:
		A=E[E.count()-1];F=A.notebook_id;G=sparta_19595da3d7(C)
		if len(G)>0:D=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=G,notebook__is_delete=0,notebook=A)|Q(is_delete=0,user=C,notebook__is_delete=0,notebook=A))
		else:D=NotebookShared.objects.filter(is_delete=0,user=C,notebook__is_delete=0,notebook=A)
		if D.count()==0:return{_B:-1,_E:_g}
	else:return{_B:-1,_E:_h}
	D=NotebookShared.objects.filter(is_owner=_A,notebook=A,user=C)
	if D.count()>0:H=datetime.now().astimezone(UTC);A.last_date_used=H;A.save()
	B=A.main_ipynb_fullpath
	if B is _D:B=os.path.join(A.project_path,_G)
	elif len(B)==0:B=os.path.join(A.project_path,_G)
	return{_B:1,_K:{'basic':{_M:A.notebook_id,_H:A.name,_P:A.slug,_Q:A.description,_S:A.is_expose_notebook,_V:A.is_public_notebook,_W:A.is_exec_code_display,_U:B,_T:A.has_password,_j:A.notebook_venv,_L:A.project_path},_i:{_k:A.lumino_layout}}}
def sparta_fb240975a1(json_data,user_obj):
	H=json_data;B=user_obj;E=H[_I];logger.debug('load_notebook DEBUG');logger.debug(E)
	if not B.is_anonymous:
		G=Notebook.objects.filter(notebook_id__startswith=E,is_delete=_C).all()
		if G.count()==1:
			A=G[G.count()-1];E=A.notebook_id;I=sparta_19595da3d7(B)
			if len(I)>0:F=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=I,notebook__is_delete=0,notebook=A)|Q(is_delete=0,user=B,notebook__is_delete=0,notebook=A)|Q(is_delete=0,notebook__is_delete=0,notebook__is_expose_notebook=_A,notebook__is_public_notebook=_A))
			else:F=NotebookShared.objects.filter(Q(is_delete=0,user=B,notebook__is_delete=0,notebook=A)|Q(is_delete=0,notebook__is_delete=0,notebook__is_expose_notebook=_A,notebook__is_public_notebook=_A))
			if F.count()==0:return{_B:-1,_E:_g}
		else:return{_B:-1,_E:_h}
	else:
		J=H.get('modalPassword',_D);logger.debug(f"DEBUG DEVELOPER VIEW TEST >>> {J}");C=sparta_8adc640bdf(E,B,password_notebook=J);logger.debug('MODAL DEBUG DEBUG DEBUG notebook_access_dict');logger.debug(C)
		if C[_B]!=1:return{_B:C[_B],_E:C[_E]}
		A=C[_J]
	if not B.is_anonymous:
		F=NotebookShared.objects.filter(is_owner=_A,notebook=A,user=B)
		if F.count()>0:K=datetime.now().astimezone(UTC);A.last_date_used=K;A.save()
	D=A.main_ipynb_fullpath
	if D is _D:D=os.path.join(A.project_path,_G)
	elif len(D)==0:D=os.path.join(A.project_path,_G)
	return{_B:1,_K:{'basic':{_M:A.notebook_id,_H:A.name,_P:A.slug,_Q:A.description,_S:A.is_expose_notebook,_V:A.is_public_notebook,_W:A.is_exec_code_display,_T:A.has_password,_j:A.notebook_venv,_L:A.project_path,_U:D},_i:{_k:A.lumino_layout}}}
def sparta_f7a2918a64(json_data,user_obj):
	I=user_obj;A=json_data;logger.debug('Save notebook');logger.debug(A);logger.debug(A.keys());N=A['isNew']
	if not N:return sparta_86674028cd(A,I)
	C=datetime.now().astimezone(UTC);J=str(uuid.uuid4());G=A[_X];E=_D
	if G:E=A[_l];E=qube_57fdffdbc8.sparta_3f3c916853(E)
	O=A[_Y];P=A[_H];Q=A[_Q];D=A[_F];D=sparta_6fbba8ac09(D);R=A[_m];S=A[_n];G=A[_X];T=A[_o];U=A.get('notebookVenv',_D);B=A[_P]
	if len(B)==0:B=A[_H]
	K=slugify(B);B=K;L=1
	while Notebook.objects.filter(slug=B).exists():B=f"{K}-{L}";L+=1
	H=_D;F=A.get(_p,_D)
	if F is not _D:
		try:
			F=F.split(',')[1];V=base64.b64decode(F);D=sparta_eb692a7fc2()[_q];M=os.path.join(D,_r,_s,_K);os.makedirs(M,exist_ok=_A);H=str(uuid.uuid4());W=os.path.join(M,f"{H}.png")
			with open(W,'wb')as X:X.write(V)
		except:pass
	Y=Notebook.objects.create(notebook_id=J,name=P,slug=B,description=Q,is_expose_notebook=R,is_public_notebook=S,has_password=G,password_e=E,is_exec_code_display=T,lumino_layout=O,project_path=D,notebook_venv=U,thumbnail_path=H,date_created=C,last_update=C,last_date_used=C,spartaqube_version=sparta_33f2973002());Z=ShareRights.objects.create(is_admin=_A,has_write_rights=_A,has_reshare_rights=_A,last_update=C);NotebookShared.objects.create(notebook=Y,user=I,share_rights=Z,is_owner=_A,date_created=C);return{_B:1,_M:J}
def sparta_86674028cd(json_data,user_obj):
	G=user_obj;B=json_data;logger.debug('Save notebook update_notebook_view');logger.debug(B);logger.debug(B.keys());L=datetime.now().astimezone(UTC);H=B[_I];I=Notebook.objects.filter(notebook_id__startswith=H,is_delete=_C).all()
	if I.count()==1:
		A=I[I.count()-1];H=A.notebook_id;M=sparta_19595da3d7(G)
		if len(M)>0:J=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=M,notebook__is_delete=0,notebook=A)|Q(is_delete=0,user=G,notebook__is_delete=0,notebook=A))
		else:J=NotebookShared.objects.filter(is_delete=0,user=G,notebook__is_delete=0,notebook=A)
		N=_C
		if J.count()>0:
			T=J[0];O=T.share_rights
			if O.is_admin or O.has_write_rights:N=_A
		if N:
			K=B[_Y];U=B[_H];V=B[_Q];W=B[_m];X=B[_n];Y=B[_X];Z=B[_o];C=B[_P]
			if A.slug!=C:
				if len(C)==0:C=B[_H]
				P=slugify(C);C=P;R=1
				while Notebook.objects.filter(slug=C).exists():C=f"{P}-{R}";R+=1
			D=_D;E=B.get(_p,_D)
			if E is not _D:
				E=E.split(',')[1];a=base64.b64decode(E)
				try:
					b=sparta_eb692a7fc2()[_q];S=os.path.join(b,_r,_s,_K);os.makedirs(S,exist_ok=_A)
					if A.thumbnail_path is _D:D=str(uuid.uuid4())
					else:D=A.thumbnail_path
					c=os.path.join(S,f"{D}.png")
					with open(c,'wb')as d:d.write(a)
				except:pass
			logger.debug('lumino_layout_dump');logger.debug(K);logger.debug(type(K));A.name=U;A.description=V;A.slug=C;A.is_expose_notebook=W;A.is_public_notebook=X;A.is_exec_code_display=Z;A.thumbnail_path=D;A.lumino_layout=K;A.last_update=L;A.last_date_used=L
			if Y:
				F=B[_l]
				if len(F)>0:F=qube_57fdffdbc8.sparta_3f3c916853(F);A.password_e=F;A.has_password=_A
			else:A.has_password=_C
			A.save()
	return{_B:1,_M:H}
def sparta_48a3fd1d19(json_data,user_obj):
	E=json_data;B=user_obj;F=E[_I];C=Notebook.objects.filter(notebook_id__startswith=F,is_delete=_C).all()
	if C.count()==1:
		A=C[C.count()-1];F=A.notebook_id;G=sparta_19595da3d7(B)
		if len(G)>0:D=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=G,notebook__is_delete=0,notebook=A)|Q(is_delete=0,user=B,notebook__is_delete=0,notebook=A))
		else:D=NotebookShared.objects.filter(is_delete=0,user=B,notebook__is_delete=0,notebook=A)
		H=_C
		if D.count()>0:
			J=D[0];I=J.share_rights
			if I.is_admin or I.has_write_rights:H=_A
		if H:K=E[_Y];A.lumino_layout=K;A.save()
	return{_B:1}
def sparta_e6137cf61a(json_data,user_obj):
	A=user_obj;G=json_data[_I];B=Notebook.objects.filter(notebook_id=G,is_delete=_C).all()
	if B.count()>0:
		C=B[B.count()-1];E=sparta_19595da3d7(A)
		if len(E)>0:D=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=E,notebook__is_delete=0,notebook=C)|Q(is_delete=0,user=A,notebook__is_delete=0,notebook=C))
		else:D=NotebookShared.objects.filter(is_delete=0,user=A,notebook__is_delete=0,notebook=C)
		if D.count()>0:F=D[0];F.is_delete=_A;F.save()
	return{_B:1}
def sparta_8adc640bdf(notebook_id,user_obj,password_notebook=_D):
	J='debug';I='Invalid password';F=password_notebook;E=notebook_id;C=user_obj;logger.debug(_M);logger.debug(E);B=Notebook.objects.filter(notebook_id__startswith=E,is_delete=_C).all();D=_C
	if B.count()==1:D=_A
	else:
		K=E;B=Notebook.objects.filter(slug__startswith=K,is_delete=_C).all()
		if B.count()==1:D=_A
	logger.debug('b_found');logger.debug(D)
	if D:
		A=B[B.count()-1];L=A.has_password
		if A.is_expose_notebook:
			logger.debug('is exposed')
			if A.is_public_notebook:
				logger.debug('is public')
				if not L:logger.debug('no password');return{_B:1,_J:A}
				else:
					logger.debug('hass password')
					if F is _D:logger.debug('empty passord provided');return{_B:2,_E:'Require password',_J:A}
					else:
						try:
							if qube_57fdffdbc8.sparta_b3ac4f618f(A.password_e)==F:return{_B:1,_J:A}
							else:return{_B:3,_E:I,_J:A}
						except Exception as M:return{_B:3,_E:I,_J:A}
			elif C.is_authenticated:
				G=sparta_19595da3d7(C)
				if len(G)>0:H=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=G,notebook__is_delete=0,notebook=A)|Q(is_delete=0,user=C,notebook__is_delete=0,notebook=A))
				else:H=NotebookShared.objects.filter(is_delete=0,user=C,notebook__is_delete=0,notebook=A)
				if H.count()>0:return{_B:1,_J:A}
			else:return{_B:-1,J:1}
	return{_B:-1,J:2}
def sparta_39646aefc5(json_data,user_obj):A=sparta_6fbba8ac09(json_data[_F]);return sparta_514ae4dea4(A)
def sparta_b48969af67(json_data,user_obj):A=sparta_6fbba8ac09(json_data[_F]);return sparta_cc0eec96cd(A)
def sparta_31452c2eae(json_data,user_obj):
	C=user_obj;B=json_data;logger.debug('notebook_ipynb_set_entrypoint json_data');logger.debug(B);F=B[_I];D=Notebook.objects.filter(notebook_id__startswith=F,is_delete=_C).all()
	if D.count()==1:
		A=D[D.count()-1];F=A.notebook_id;G=sparta_19595da3d7(C)
		if len(G)>0:E=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=G,notebook__is_delete=0,notebook=A)|Q(is_delete=0,user=C,notebook__is_delete=0,notebook=A))
		else:E=NotebookShared.objects.filter(is_delete=0,user=C,notebook__is_delete=0,notebook=A)
		H=_C
		if E.count()>0:
			J=E[0];I=J.share_rights
			if I.is_admin or I.has_write_rights:H=_A
		if H:K=sparta_6fbba8ac09(B['fullPath']);A.main_ipynb_fullpath=K;A.save()
	return{_B:1}
async def notebook_permission_code_exec(json_data):
	G='source';F='cellId';C=json_data;logger.debug('Callilng notebook_permission_code_exec')
	try:
		H=C[_I];D=Notebook.objects.filter(notebook_id__startswith=H,is_delete=_C)
		if await D.acount()>0:
			E=await D.afirst();I=C[F];A=E.main_ipynb_fullpath
			if A is _D:A=os.path.join(E.project_path,_G)
			J=qube_952fdf29a0.sparta_0e487626ba(A);K=J['cells']
			for B in K:
				L=json.loads(B['metadata']['sqMetadata'])
				if L[F]==I:logger.debug('Found Cell Code');logger.debug(B[G][0]);return B[G][0]
	except Exception as M:logger.debug('Except is:');logger.debug(M);return''
	return''
def sparta_653de968ff(json_data,user_obj):0
from django.core.management import call_command
from io import StringIO
def sparta_50fa11f2aa(project_path,python_executable=_R):
	C=python_executable;B=project_path;A=_C
	try:
		I=os.path.join(B,_N)
		if not os.path.exists(I):A=_A;return _C,f"Error: manage.py not found in {B}",A
		F=os.environ.copy();F[_t]=_u;G=sparta_9cd4a03989()
		if sys.platform==_Z:C=os.path.join(G,_a,_v)
		else:C=os.path.join(G,_b,_R)
		J=[C,_N,_w,'--dry-run'];D=subprocess.run(J,cwd=B,text=_A,capture_output=_A,env=F)
		if D.returncode!=0:A=_A;return _C,f"Error: {D.stderr}",A
		H=D.stdout;K='No changes detected'not in H;return K,H,A
	except FileNotFoundError as E:A=_A;return _C,f"Error: {E}. Ensure the correct Python executable and project path.",A
	except Exception as E:A=_A;return _C,str(E),A
def sparta_9cd4a03989():
	A=os.environ.get('VIRTUAL_ENV')
	if A:return A
	else:return sys.prefix
def sparta_4e50d2e043():
	A=sparta_9cd4a03989()
	if sys.platform==_Z:B=os.path.join(A,_a,'pip.exe')
	else:B=os.path.join(A,_b,'pip')
	return B
def sparta_44155577f1(json_data,user_obj):
	D=sparta_6fbba8ac09(json_data[_F]);A=D;B=os.path.join(sparta_eb692a7fc2()[_c],_K,_d);C=os.path.join(A,_O)
	if not os.path.exists(C):os.makedirs(C)
	shutil.copytree(os.path.join(B,_O),C,dirs_exist_ok=_A);logger.debug(f"Folder copied from {B} to {A}");shutil.copy2(os.path.join(B,_e),A);shutil.copy2(os.path.join(B,_f),A);return{_B:1}
def sparta_f69d6580ea(json_data,user_obj):
	A=sparta_6fbba8ac09(json_data[_F]);A=os.path.join(A,_O);G,C,D=sparta_50fa11f2aa(A);B=_A;E=1;F=''
	if D:
		E=-1;F=C;B;H=os.path.join(A,_N)
		if not os.path.exists(H):B=_C
	I={_B:E,'has_error':D,'has_pending_migrations':G,_x:C,_E:F,'has_django_init':B};return I
def sparta_c5333e92ff(project_path,python_executable=_R):
	D=project_path;B=python_executable
	try:
		H=os.path.join(D,_N)
		if not os.path.exists(H):return _C,f"Error: manage.py not found in {D}"
		F=os.environ.copy();F[_t]=_u;G=sparta_9cd4a03989()
		if sys.platform==_Z:B=os.path.join(G,_a,_v)
		else:B=os.path.join(G,_b,_R)
		I=[[B,_N,_w],[B,_N,'migrate']];C=[]
		for J in I:
			A=subprocess.run(J,cwd=D,text=_A,capture_output=_A,env=F)
			if A.stdout is not _D:
				if len(str(A.stdout))>0:C.append(A.stdout)
			if A.stderr is not _D:
				if len(str(A.stderr))>0:C.append(f"<span style='color:red'>Stderr:\n{A.stderr}</span>")
			if A.returncode!=0:return _C,'\n'.join(C)
		return _A,'\n'.join(C)
	except FileNotFoundError as E:return _C,f"Error: {E}. Ensure the correct Python executable and project path."
	except Exception as E:return _C,str(E)
def sparta_d6ba999974(json_data,user_obj):
	A=sparta_6fbba8ac09(json_data[_F]);A=os.path.join(A,_O);B,C=sparta_c5333e92ff(A);D=1;E=''
	if not B:D=-1;E=C
	return{_B:D,'res_migration':B,_x:C,_E:E}
def sparta_b22a8cb6c5(json_data,user_obj):return{_B:1}
def sparta_a4896004c1(json_data,user_obj):return{_B:1}