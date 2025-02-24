_U='projectPath'
_T='kernelSize'
_S='kernelVenv'
_R='kernel_size'
_Q='main_ipynb_fullpath'
_P='kernel_manager_uuid'
_O='main.ipynb'
_N='-kernel__last_update'
_M='kernel_cpkl_unpicklable'
_L='windows'
_K='luminoLayout'
_J='description'
_I='slug'
_H='is_static_variables'
_G=False
_F='unpicklable'
_E='name'
_D='kernelManagerUUID'
_C='res'
_B=True
_A=None
import os,sys,gc,json,base64,shutil,zipfile,io,uuid,subprocess,cloudpickle,platform,getpass
from django.conf import settings
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
from pathlib import Path
from dateutil import parser
import pytz
UTC=pytz.utc
from django.contrib.humanize.templatetags.humanize import naturalday
from project.sparta_0c8b5020ad.sparta_da6af08d87 import qube_c77b125770 as qube_c77b125770
from project.models_spartaqube import Kernel,KernelShared,ShareRights
from project.sparta_0c8b5020ad.sparta_ff964033dc.qube_7f42fde550 import IPythonKernel as IPythonKernel
from project.sparta_0c8b5020ad.sparta_2b5b2a60e0.qube_979597c799 import sparta_2d3e41973b,sparta_16309ca73f
from project.sparta_0c8b5020ad.sparta_98d93fe84a.qube_8d4f2124f6 import sparta_449f6f558b,sparta_ad7cac9d75,sparta_6a3ed20c7c,sparta_e232e2761b
from project.sparta_0c8b5020ad.sparta_2b5b2a60e0.qube_d0cd55cc8e import sparta_9e4c08aad7,sparta_edd7905d33
from project.sparta_0c8b5020ad.sparta_4a8796c17c.qube_64f888aab6 import sparta_a9f5c412a4
from project.logger_config import logger
def sparta_7e22b2c145():
	A=platform.system()
	if A=='Windows':return _L
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
def sparta_6e1aa35871():
	A=sparta_7e22b2c145()
	if A==_L:B=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\kernel"
	elif A=='linux':B=os.path.expanduser('~/SpartaQube/kernel')
	elif A=='mac':B=os.path.expanduser('~/Library/Application Support\\SpartaQube\\kernel')
	return B
def sparta_ee84d75df3(user_obj):
	A=qube_c77b125770.sparta_75b909e585(user_obj)
	if len(A)>0:B=[A.user_group for A in A]
	else:B=[]
	return B
def sparta_9b27394b91(user_obj,kernel_manager_uuid):from project.sparta_0c8b5020ad.sparta_87e47ed0f0 import qube_40c1566c0a as B;E=B.sparta_8d78924390(user_obj,kernel_manager_uuid);A=B.sparta_cfe0d0fe4f(E);logger.debug('get_cloudpickle_kernel_variables res_dict');logger.debug(A);C=A['picklable'];logger.debug('kernel_cpkl_picklable');logger.debug(type(C));logger.debug("res_dict['unpicklable']");logger.debug(type(A[_F]));D=cloudpickle.loads(A[_F]);logger.debug(_M);logger.debug(type(D));return C,D
def sparta_2dfd21a2c5(user_obj):
	I='%Y-%m-%d';C=user_obj;J=sparta_6e1aa35871();D=sparta_ee84d75df3(C)
	if len(D)>0:B=KernelShared.objects.filter(Q(is_delete=0,user_group__in=D,kernel__is_delete=0)|Q(is_delete=0,user=C,kernel__is_delete=0))
	else:B=KernelShared.objects.filter(Q(is_delete=0,user=C,kernel__is_delete=0))
	if B.count()>0:B=B.order_by(_N)
	E=[]
	for F in B:
		A=F.kernel;K=F.share_rights;G=_A
		try:G=str(A.last_update.strftime(I))
		except:pass
		H=_A
		try:H=str(A.date_created.strftime(I))
		except Exception as L:logger.debug(L)
		M=os.path.join(J,A.kernel_manager_uuid,_O);E.append({_P:A.kernel_manager_uuid,_E:A.name,_I:A.slug,_J:A.description,_Q:M,_R:A.kernel_size,'has_write_rights':K.has_write_rights,'last_update':G,'date_created':H})
	return E
def sparta_c79ce07be7(user_obj):
	B=user_obj;C=sparta_ee84d75df3(B)
	if len(C)>0:A=KernelShared.objects.filter(Q(is_delete=0,user_group__in=C,kernel__is_delete=0)|Q(is_delete=0,user=B,kernel__is_delete=0))
	else:A=KernelShared.objects.filter(Q(is_delete=0,user=B,kernel__is_delete=0))
	if A.count()>0:A=A.order_by(_N);return[A.kernel.kernel_manager_uuid for A in A]
	return[]
def sparta_333d575a4f(user_obj,kernel_manager_uuid):
	B=user_obj;D=Kernel.objects.filter(kernel_manager_uuid=kernel_manager_uuid).all()
	if D.count()>0:
		A=D[0];E=sparta_ee84d75df3(B)
		if len(E)>0:C=KernelShared.objects.filter(Q(is_delete=0,user_group__in=E,kernel__is_delete=0,kernel=A)|Q(is_delete=0,user=B,kernel__is_delete=0,kernel=A))
		else:C=KernelShared.objects.filter(is_delete=0,user=B,kernel__is_delete=0,kernel=A)
		F=_G
		if C.count()>0:
			H=C[0];G=H.share_rights
			if G.is_admin or G.has_write_rights:F=_B
		if F:return A
def sparta_e9ce85a77f(json_data,user_obj):
	D=user_obj;from project.sparta_0c8b5020ad.sparta_87e47ed0f0 import qube_40c1566c0a as I;A=json_data[_D];B=I.sparta_8d78924390(D,A)
	if B is _A:return{_C:-1,'errorMsg':'Kernel not found'}
	E=sparta_6e1aa35871();J=os.path.join(E,A,_O);K=B.venv_name;F=_A;G=_G;H=_G;C=sparta_333d575a4f(D,A)
	if C is not _A:G=_B;F=C.lumino_layout;H=C.is_static_variables
	return{_C:1,'kernel':{'basic':{'is_kernel_saved':G,_H:H,_P:A,_E:B.name,'kernel_venv':K,'kernel_type':B.type,'project_path':E,_Q:J},'lumino':{'lumino_layout':F}}}
def sparta_6603ec0107(json_data,user_obj):
	D=user_obj;A=json_data;logger.debug('Save notebook');logger.debug(A);logger.debug(A.keys());L=A['isKernelSaved']
	if L:return sparta_0a24e0f9d1(A,D)
	C=datetime.now().astimezone(UTC);G=A[_D];M=A[_K];N=A[_E];O=A[_J];E=sparta_6e1aa35871();E=sparta_2d3e41973b(E);H=A[_H];P=A.get(_S,_A);Q=A.get(_T,0);B=A.get(_I,'')
	if len(B)==0:B=A[_E]
	I=slugify(B);B=I;J=1
	while Kernel.objects.filter(slug=B).exists():B=f"{I}-{J}";J+=1
	K=_A;F=[]
	if H:K,F=sparta_9b27394b91(D,G)
	R=Kernel.objects.create(kernel_manager_uuid=G,name=N,slug=B,description=O,is_static_variables=H,lumino_layout=M,project_path=E,kernel_venv=P,kernel_variables=K,kernel_size=Q,date_created=C,last_update=C,last_date_used=C,spartaqube_version=sparta_a9f5c412a4());S=ShareRights.objects.create(is_admin=_B,has_write_rights=_B,has_reshare_rights=_B,last_update=C);KernelShared.objects.create(kernel=R,user=D,share_rights=S,is_owner=_B,date_created=C);logger.debug(_M);logger.debug(F);return{_C:1,_F:F}
def sparta_0a24e0f9d1(json_data,user_obj):
	F=user_obj;A=json_data;logger.debug('update_kernel_notebook');logger.debug(A);D=A[_D];B=sparta_333d575a4f(F,D)
	if B is not _A:
		K=datetime.now().astimezone(UTC);D=A[_D];L=A[_K];M=A[_E];N=A[_J];E=A[_H];O=A.get(_S,_A);P=A.get(_T,0);C=A.get(_I,'')
		if len(C)==0:C=A[_E]
		G=slugify(C);C=G;H=1
		while Kernel.objects.filter(slug=C).exists():C=f"{G}-{H}";H+=1
		E=A[_H];I=_A;J=[]
		if E:I,J=sparta_9b27394b91(F,D)
		B.name=M;B.description=N;B.slug=C;B.kernel_venv=O;B.kernel_size=P;B.is_static_variables=E;B.kernel_variables=I;B.lumino_layout=L;B.last_update=K;B.save()
	return{_C:1,_F:J}
def sparta_57c5d36625(json_data,user_obj):0
def sparta_9e993d3da5(json_data,user_obj):A=sparta_2d3e41973b(json_data[_U]);return sparta_9e4c08aad7(A)
def sparta_976db41fda(json_data,user_obj):A=sparta_2d3e41973b(json_data[_U]);return sparta_edd7905d33(A)
def sparta_9bfa4d434c(json_data,user_obj):
	C=user_obj;B=json_data;logger.debug('SAVE LYUMINO LAYOUT KERNEL NOTEBOOK');logger.debug('json_data');logger.debug(B);I=B[_D];E=Kernel.objects.filter(kernel_manager_uuid=I).all()
	if E.count()>0:
		A=E[0];F=sparta_ee84d75df3(C)
		if len(F)>0:D=KernelShared.objects.filter(Q(is_delete=0,user_group__in=F,kernel__is_delete=0,kernel=A)|Q(is_delete=0,user=C,kernel__is_delete=0,kernel=A))
		else:D=KernelShared.objects.filter(is_delete=0,user=C,kernel__is_delete=0,kernel=A)
		G=_G
		if D.count()>0:
			J=D[0];H=J.share_rights
			if H.is_admin or H.has_write_rights:G=_B
		if G:K=B[_K];A.lumino_layout=K;A.save()
	return{_C:1}
def sparta_1ec2d55ffa(json_data,user_obj):
	from project.sparta_0c8b5020ad.sparta_87e47ed0f0 import qube_40c1566c0a as A;C=json_data[_D];B=A.sparta_8d78924390(user_obj,C)
	if B is not _A:D=A.sparta_a657347f33(B);return{_C:1,_R:D}
	return{_C:-1}
def sparta_9189b26ab1(json_data,user_obj):
	B=json_data[_D];A=sparta_333d575a4f(user_obj,B)
	if A is not _A:A.is_delete=_B;A.save()
	return{_C:1}