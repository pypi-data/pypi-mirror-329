_q='makemigrations'
_p='python.exe'
_o='app.settings'
_n='DJANGO_SETTINGS_MODULE'
_m='thumbnail'
_l='previewImage'
_k='isPublic'
_j='isExpose'
_i='password'
_h='lumino_layout'
_g='developer_venv'
_f='lumino'
_e='Project not found...'
_d='You do not have the rights to access this project'
_c='backend'
_b='bin'
_a='Scripts'
_Z='win32'
_Y='stdout'
_X='npm'
_W='luminoLayout'
_V='hasPassword'
_U='is_public_developer'
_T='has_password'
_S='is_expose_developer'
_R='static'
_Q='python'
_P='frontend'
_O='manage.py'
_N='developerId'
_M='description'
_L='slug'
_K='project_path'
_J='developer_id'
_I='developer'
_H='developer_obj'
_G='name'
_F='projectPath'
_E=None
_D='errorMsg'
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
from project.models_spartaqube import Developer,DeveloperShared
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
def sparta_be1c3c44aa():
	A=['esbuild-darwin-arm64','esbuild-darwin-x64','esbuild-linux-x64','esbuild-windows-x64.exe'];C=os.path.dirname(__file__);A=[os.path.join(C,'esbuild',A)for A in A]
	def D(file_path):
		A=file_path
		if os.name=='nt':
			try:subprocess.run(['icacls',A,'/grant','*S-1-1-0:(RX)'],check=_A);logger.debug(f"Executable permissions set for: {A} (Windows)")
			except subprocess.CalledProcessError as B:logger.debug(f"Failed to set permissions for {A} on Windows: {B}")
		else:
			try:os.chmod(A,stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH);logger.debug(f"Executable permissions set for: {A} (Unix/Linux/Mac)")
			except Exception as B:logger.debug(f"Failed to set permissions for {A} on Unix/Linux: {B}")
	for B in A:
		if os.path.exists(B):D(B)
		else:logger.debug(f"File not found: {B}")
	return{_B:1}
def sparta_19595da3d7(user_obj):
	A=qube_60ba9e4a49.sparta_88c03c9ba1(user_obj)
	if len(A)>0:B=[A.user_group for A in A]
	else:B=[]
	return B
def sparta_f1982996cd(project_path):
	G='template';A=project_path
	if not os.path.exists(A):os.makedirs(A)
	D=A;H=os.path.dirname(__file__);E=os.path.join(sparta_eb692a7fc2()['django_app_template'],_I,G)
	for F in os.listdir(E):
		C=os.path.join(E,F);B=os.path.join(D,F)
		if os.path.isdir(C):shutil.copytree(C,B,dirs_exist_ok=_A)
		else:shutil.copy2(C,B)
	I=os.path.dirname(os.path.dirname(H));J=os.path.dirname(I);K=os.path.join(J,_R);L=os.path.join(K,'js',_I,G,_P);B=os.path.join(D,_P);shutil.copytree(L,B,dirs_exist_ok=_A);return{_K:A}
def sparta_81922a6acf(json_data,user_obj):
	B=user_obj;A=json_data[_F];A=sparta_6fbba8ac09(A);F=Developer.objects.filter(project_path=A).all()
	if F.count()>0:
		C=F[0];G=sparta_19595da3d7(B)
		if len(G)>0:D=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=G,developer__is_delete=0,developer=C)|Q(is_delete=0,user=B,developer__is_delete=0,developer=C))
		else:D=DeveloperShared.objects.filter(is_delete=0,user=B,developer__is_delete=0,developer=C)
		H=_C
		if D.count()>0:
			J=D[0];I=J.share_rights
			if I.is_admin or I.has_write_rights:H=_A
		if not H:return{_B:-1,_D:'Chose another path. A project already exists at this location'}
	if not isinstance(A,str):return{_B:-1,_D:'Project path must be a string.'}
	try:A=os.path.abspath(A)
	except Exception as E:return{_B:-1,_D:f"Invalid project path: {str(E)}"}
	try:
		if not os.path.exists(A):os.makedirs(A)
		K=sparta_f1982996cd(A);A=K[_K];return{_B:1,_K:A}
	except Exception as E:return{_B:-1,_D:f"Failed to create folder: {str(E)}"}
def sparta_224028319d(json_data,user_obj):A=json_data;A['bAddGitignore']=_A;A['bAddReadme']=_A;return qube_2025927415.sparta_fd68c1ddb5(A,user_obj)
def sparta_a136db35e2(json_data,user_obj):return sparta_9889473ef7(json_data,user_obj)
def sparta_01bbccd51d(json_data,user_obj):
	K='%Y-%m-%d';J='Recently used';D=user_obj;F=sparta_19595da3d7(D)
	if len(F)>0:A=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=F,developer__is_delete=0)|Q(is_delete=0,user=D,developer__is_delete=0)|Q(is_delete=0,developer__is_delete=0,developer__is_expose_developer=_A,developer__is_public_developer=_A))
	else:A=DeveloperShared.objects.filter(Q(is_delete=0,user=D,developer__is_delete=0)|Q(is_delete=0,developer__is_delete=0,developer__is_expose_developer=_A,developer__is_public_developer=_A))
	if A.count()>0:
		C=json_data.get('orderBy',J)
		if C==J:A=A.order_by('-developer__last_date_used')
		elif C=='Date desc':A=A.order_by('-developer__last_update')
		elif C=='Date asc':A=A.order_by('developer__last_update')
		elif C=='Name desc':A=A.order_by('-developer__name')
		elif C=='Name asc':A=A.order_by('developer__name')
	G=[]
	for E in A:
		B=E.developer;L=E.share_rights;H=_E
		try:H=str(B.last_update.strftime(K))
		except:pass
		I=_E
		try:I=str(B.date_created.strftime(K))
		except Exception as M:logger.debug(M)
		G.append({_J:B.developer_id,_G:B.name,_L:B.slug,_M:B.description,_S:B.is_expose_developer,_T:B.has_password,_U:B.is_public_developer,'is_owner':E.is_owner,'has_write_rights':L.has_write_rights,'last_update':H,'date_created':I})
	return{_B:1,'developer_library':G}
def sparta_aa57198e95(json_data,user_obj):
	B=user_obj;E=json_data[_N];D=Developer.objects.filter(developer_id__startswith=E,is_delete=_C).all()
	if D.count()==1:
		A=D[D.count()-1];E=A.developer_id;F=sparta_19595da3d7(B)
		if len(F)>0:C=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=F,developer__is_delete=0,developer=A)|Q(is_delete=0,user=B,developer__is_delete=0,developer=A))
		else:C=DeveloperShared.objects.filter(is_delete=0,user=B,developer__is_delete=0,developer=A)
		if C.count()==0:return{_B:-1,_D:_d}
	else:return{_B:-1,_D:_e}
	C=DeveloperShared.objects.filter(is_owner=_A,developer=A,user=B)
	if C.count()>0:G=datetime.now().astimezone(UTC);A.last_date_used=G;A.save()
	return{_B:1,_I:{'basic':{_J:A.developer_id,_G:A.name,_L:A.slug,_M:A.description,_S:A.is_expose_developer,_U:A.is_public_developer,_T:A.has_password,_g:A.developer_venv,_K:A.project_path},_f:{_h:A.lumino_layout}}}
def sparta_b2c3d27566(json_data,user_obj):
	G=json_data;B=user_obj;E=G[_N]
	if not B.is_anonymous:
		F=Developer.objects.filter(developer_id__startswith=E,is_delete=_C).all()
		if F.count()==1:
			A=F[F.count()-1];E=A.developer_id;H=sparta_19595da3d7(B)
			if len(H)>0:D=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=H,developer__is_delete=0,developer=A)|Q(is_delete=0,user=B,developer__is_delete=0,developer=A)|Q(is_delete=0,developer__is_delete=0,developer__is_expose_developer=_A,developer__is_public_developer=_A))
			else:D=DeveloperShared.objects.filter(Q(is_delete=0,user=B,developer__is_delete=0,developer=A)|Q(is_delete=0,developer__is_delete=0,developer__is_expose_developer=_A,developer__is_public_developer=_A))
			if D.count()==0:return{_B:-1,_D:_d}
		else:return{_B:-1,_D:_e}
	else:
		I=G.get('modalPassword',_E);logger.debug(f"DEBUG DEVELOPER VIEW TEST >>> {I}");C=has_developer_access(E,B,password_developer=I);logger.debug('MODAL DEBUG DEBUG DEBUG developer_access_dict');logger.debug(C)
		if C[_B]!=1:return{_B:C[_B],_D:C[_D]}
		A=C[_H]
	if not B.is_anonymous:
		D=DeveloperShared.objects.filter(is_owner=_A,developer=A,user=B)
		if D.count()>0:J=datetime.now().astimezone(UTC);A.last_date_used=J;A.save()
	return{_B:1,_I:{'basic':{_J:A.developer_id,_G:A.name,_L:A.slug,_M:A.description,_S:A.is_expose_developer,_U:A.is_public_developer,_T:A.has_password,_g:A.developer_venv,_K:A.project_path},_f:{_h:A.lumino_layout}}}
def sparta_ec869d77c3(json_data,user_obj):
	I=user_obj;A=json_data;N=A['isNew']
	if not N:return sparta_4dc2be4850(A,I)
	C=datetime.now().astimezone(UTC);J=str(uuid.uuid4());G=A[_V];E=_E
	if G:E=A[_i];E=qube_57fdffdbc8.sparta_3f3c916853(E)
	O=A[_W];P=A[_G];Q=A[_M];D=A[_F];D=sparta_6fbba8ac09(D);R=A[_j];S=A[_k];G=A[_V];T=A.get('developerVenv',_E);B=A[_L]
	if len(B)==0:B=A[_G]
	K=slugify(B);B=K;L=1
	while Developer.objects.filter(slug=B).exists():B=f"{K}-{L}";L+=1
	H=_E;F=A.get(_l,_E)
	if F is not _E:
		try:
			F=F.split(',')[1];U=base64.b64decode(F);V=os.path.dirname(__file__);D=os.path.dirname(os.path.dirname(os.path.dirname(V)));M=os.path.join(D,_R,_m,_I);os.makedirs(M,exist_ok=_A);H=str(uuid.uuid4());W=os.path.join(M,f"{H}.png")
			with open(W,'wb')as X:X.write(U)
		except:pass
	Y=Developer.objects.create(developer_id=J,name=P,slug=B,description=Q,is_expose_developer=R,is_public_developer=S,has_password=G,password_e=E,lumino_layout=O,project_path=D,developer_venv=T,thumbnail_path=H,date_created=C,last_update=C,last_date_used=C,spartaqube_version=sparta_33f2973002());Z=ShareRights.objects.create(is_admin=_A,has_write_rights=_A,has_reshare_rights=_A,last_update=C);DeveloperShared.objects.create(developer=Y,user=I,share_rights=Z,is_owner=_A,date_created=C);return{_B:1,_J:J}
def sparta_4dc2be4850(json_data,user_obj):
	G=user_obj;B=json_data;L=datetime.now().astimezone(UTC);H=B[_N];I=Developer.objects.filter(developer_id__startswith=H,is_delete=_C).all()
	if I.count()==1:
		A=I[I.count()-1];H=A.developer_id;M=sparta_19595da3d7(G)
		if len(M)>0:J=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=M,developer__is_delete=0,developer=A)|Q(is_delete=0,user=G,developer__is_delete=0,developer=A))
		else:J=DeveloperShared.objects.filter(is_delete=0,user=G,developer__is_delete=0,developer=A)
		N=_C
		if J.count()>0:
			T=J[0];O=T.share_rights
			if O.is_admin or O.has_write_rights:N=_A
		if N:
			K=B[_W];U=B[_G];V=B[_M];W=B[_j];X=B[_k];Y=B[_V];C=B[_L]
			if A.slug!=C:
				if len(C)==0:C=B[_G]
				P=slugify(C);C=P;R=1
				while Developer.objects.filter(slug=C).exists():C=f"{P}-{R}";R+=1
			D=_E;E=B.get(_l,_E)
			if E is not _E:
				E=E.split(',')[1];Z=base64.b64decode(E)
				try:
					a=os.path.dirname(__file__);b=os.path.dirname(os.path.dirname(os.path.dirname(a)));S=os.path.join(b,_R,_m,_I);os.makedirs(S,exist_ok=_A)
					if A.thumbnail_path is _E:D=str(uuid.uuid4())
					else:D=A.thumbnail_path
					c=os.path.join(S,f"{D}.png")
					with open(c,'wb')as d:d.write(Z)
				except:pass
			logger.debug('lumino_layout_dump');logger.debug(K);logger.debug(type(K));A.name=U;A.description=V;A.slug=C;A.is_expose_developer=W;A.is_public_developer=X;A.thumbnail_path=D;A.lumino_layout=K;A.last_update=L;A.last_date_used=L
			if Y:
				F=B[_i]
				if len(F)>0:F=qube_57fdffdbc8.sparta_3f3c916853(F);A.password_e=F;A.has_password=_A
			else:A.has_password=_C
			A.save()
	return{_B:1,_J:H}
def sparta_f0373947fe(json_data,user_obj):
	E=json_data;B=user_obj;F=E[_N];C=Developer.objects.filter(developer_id__startswith=F,is_delete=_C).all()
	if C.count()==1:
		A=C[C.count()-1];F=A.developer_id;G=sparta_19595da3d7(B)
		if len(G)>0:D=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=G,developer__is_delete=0,developer=A)|Q(is_delete=0,user=B,developer__is_delete=0,developer=A))
		else:D=DeveloperShared.objects.filter(is_delete=0,user=B,developer__is_delete=0,developer=A)
		H=_C
		if D.count()>0:
			J=D[0];I=J.share_rights
			if I.is_admin or I.has_write_rights:H=_A
		if H:K=E[_W];A.lumino_layout=K;A.save()
	return{_B:1}
def sparta_b19c8e0823(json_data,user_obj):
	A=user_obj;G=json_data[_N];B=Developer.objects.filter(developer_id=G,is_delete=_C).all()
	if B.count()>0:
		C=B[B.count()-1];E=sparta_19595da3d7(A)
		if len(E)>0:D=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=E,developer__is_delete=0,developer=C)|Q(is_delete=0,user=A,developer__is_delete=0,developer=C))
		else:D=DeveloperShared.objects.filter(is_delete=0,user=A,developer__is_delete=0,developer=C)
		if D.count()>0:F=D[0];F.is_delete=_A;F.save()
	return{_B:1}
def has_developer_access(developer_id,user_obj,password_developer=_E):
	J='debug';I='Invalid password';F=password_developer;E=developer_id;C=user_obj;logger.debug(_J);logger.debug(E);B=Developer.objects.filter(developer_id__startswith=E,is_delete=_C).all();D=_C
	if B.count()==1:D=_A
	else:
		K=E;B=Developer.objects.filter(slug__startswith=K,is_delete=_C).all()
		if B.count()==1:D=_A
	logger.debug('b_found');logger.debug(D)
	if D:
		A=B[B.count()-1];L=A.has_password
		if A.is_expose_developer:
			logger.debug('is exposed')
			if A.is_public_developer:
				logger.debug('is public')
				if not L:logger.debug('no password');return{_B:1,_H:A}
				else:
					logger.debug('hass password')
					if F is _E:logger.debug('empty passord provided');return{_B:2,_D:'Require password',_H:A}
					else:
						try:
							if qube_57fdffdbc8.sparta_b3ac4f618f(A.password_e)==F:return{_B:1,_H:A}
							else:return{_B:3,_D:I,_H:A}
						except Exception as M:return{_B:3,_D:I,_H:A}
			elif C.is_authenticated:
				G=sparta_19595da3d7(C)
				if len(G)>0:H=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=G,developer__is_delete=0,developer=A)|Q(is_delete=0,user=C,developer__is_delete=0,developer=A))
				else:H=DeveloperShared.objects.filter(is_delete=0,user=C,developer__is_delete=0,developer=A)
				if H.count()>0:return{_B:1,_H:A}
			else:return{_B:-1,J:1}
	return{_B:-1,J:2}
def sparta_8756e05fdc(json_data,user_obj):A=sparta_6fbba8ac09(json_data[_F]);return sparta_514ae4dea4(A)
def sparta_c9c0a508ae(json_data,user_obj):A=sparta_6fbba8ac09(json_data[_F]);return sparta_cc0eec96cd(A)
def sparta_6eabf175e9():
	try:
		if platform.system()=='Windows':subprocess.run(['where',_X],capture_output=_A,check=_A)
		else:subprocess.run(['command','-v',_X],capture_output=_A,check=_A)
		return _A
	except subprocess.CalledProcessError:return _C
	except FileNotFoundError:return _C
def sparta_d4fe486f43():
	try:A=subprocess.run('npm -v',shell=_A,capture_output=_A,text=_A,check=_A);return A.stdout
	except:
		try:A=subprocess.run([_X,'-v'],capture_output=_A,text=_A,check=_A);return A.stdout.strip()
		except Exception as B:logger.debug(B);return
def sparta_ffc24fde28():
	try:A=subprocess.run('node -v',shell=_A,capture_output=_A,text=_A,check=_A);return A.stdout
	except:
		try:A=subprocess.run(['node','-v'],capture_output=_A,text=_A,check=_A);return A.stdout.strip()
		except Exception as B:logger.debug(B);return
def sparta_917f07c9d3(json_data,user_obj):
	A=sparta_6fbba8ac09(json_data[_F]);A=os.path.join(A,_P)
	if not os.path.isdir(A):return{_B:-1,_D:f"The provided path '{A}' is not a valid directory."}
	B=os.path.join(A,'package.json');C=os.path.exists(B);D=sparta_6eabf175e9();return{_B:1,'is_init':C,'is_npm_installed':D,'npm_version':sparta_d4fe486f43(),'node_version':sparta_ffc24fde28()}
def sparta_9889473ef7(json_data,user_obj):
	A=sparta_6fbba8ac09(json_data[_F]);A=os.path.join(A,_P)
	try:C=subprocess.run('npm init -y',shell=_A,capture_output=_A,text=_A,check=_A,cwd=A);logger.debug(C.stdout);return{_B:1}
	except Exception as B:logger.debug('Error node npm init');logger.debug(B);return{_B:-1,_D:str(B)}
def sparta_e0f04d183e(json_data,user_obj):
	A=json_data;logger.debug('NODE LIS LIBS');logger.debug(A);D=sparta_6fbba8ac09(A[_F])
	try:B=subprocess.run('npm list',shell=_A,capture_output=_A,text=_A,check=_A,cwd=D);logger.debug(B.stdout);return{_B:1,_Y:B.stdout}
	except Exception as C:logger.debug('Exception');logger.debug(C);return{_B:-1,_D:str(C)}
from django.core.management import call_command
from io import StringIO
def sparta_50fa11f2aa(project_path,python_executable=_Q):
	C=python_executable;B=project_path;A=_C
	try:
		I=os.path.join(B,_O)
		if not os.path.exists(I):A=_A;return _C,f"Error: manage.py not found in {B}",A
		F=os.environ.copy();F[_n]=_o;G=sparta_9cd4a03989()
		if sys.platform==_Z:C=os.path.join(G,_a,_p)
		else:C=os.path.join(G,_b,_Q)
		J=[C,_O,_q,'--dry-run'];D=subprocess.run(J,cwd=B,text=_A,capture_output=_A,env=F)
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
def sparta_7d2abbce7c(json_data,user_obj):
	A=sparta_6fbba8ac09(json_data[_F]);A=os.path.join(A,_c,'app');F,B,C=sparta_50fa11f2aa(A);D=1;E=''
	if C:D=-1;E=B
	return{_B:D,'has_error':C,'has_pending_migrations':F,_Y:B,_D:E}
def sparta_c5333e92ff(project_path,python_executable=_Q):
	D=project_path;B=python_executable
	try:
		I=os.path.join(D,_O)
		if not os.path.exists(I):return _C,f"Error: manage.py not found in {D}"
		F=os.environ.copy();F[_n]=_o;G=sparta_9cd4a03989()
		if sys.platform==_Z:B=os.path.join(G,_a,_p)
		else:B=os.path.join(G,_b,_Q)
		H=[[B,_O,_q],[B,_O,'migrate']];logger.debug('commands');logger.debug(H);C=[]
		for J in H:
			A=subprocess.run(J,cwd=D,text=_A,capture_output=_A,env=F)
			if A.stdout is not _E:
				if len(str(A.stdout))>0:C.append(A.stdout)
			if A.stderr is not _E:
				if len(str(A.stderr))>0:C.append(f"<span style='color:red'>Stderr:\n{A.stderr}</span>")
			if A.returncode!=0:return _C,'\n'.join(C)
		return _A,'\n'.join(C)
	except FileNotFoundError as E:return _C,f"Error: {E}. Ensure the correct Python executable and project path."
	except Exception as E:return _C,str(E)
def sparta_b6444fca10(json_data,user_obj):
	A=sparta_6fbba8ac09(json_data[_F]);A=os.path.join(A,_c,'app');B,C=sparta_c5333e92ff(A);D=1;E=''
	if not B:D=-1;E=C
	return{_B:D,'res_migration':B,_Y:C,_D:E}
def sparta_777dad43df(json_data,user_obj):return{_B:1}
def sparta_b22a8cb6c5(json_data,user_obj):return{_B:1}
def sparta_126e76b439(json_data,user_obj):return{_B:1}
def sparta_781c2f70e2(json_data,user_obj):logger.debug('developer_hot_reload_preview json_data');logger.debug(json_data);return{_B:1}
def sparta_abcbafa205(json_data,user_obj):
	C='baseProjectPath';A=json_data;D=sparta_6fbba8ac09(A[C]);E=os.path.join(os.path.dirname(D),_c);sys.path.insert(0,E);import webservices as B;importlib.reload(B);F=A['service'];G=A.copy();del A[C]
	try:return B.sparta_89e9f27ee5(F,G,user_obj)
	except Exception as H:return{_B:-1,_D:str(H)}