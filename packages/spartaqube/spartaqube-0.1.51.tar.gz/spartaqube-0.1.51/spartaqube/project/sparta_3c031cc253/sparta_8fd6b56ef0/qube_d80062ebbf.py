_D='manifest'
_C=None
_B=False
_A=True
import os,socket,json,requests
from datetime import date,datetime
from project.models import UserProfile,AppVersioning
from django.conf import settings as conf_settings
from spartaqube_app.secrets import sparta_41cb52c24c
from spartaqube_app.path_mapper_obf import sparta_638705750a
from project.sparta_ab7a1c0e2d.sparta_969a0318d0.qube_239a17d111 import sparta_e9605efc3e
import pytz
UTC=pytz.utc
class dotdict(dict):__getattr__=dict.get;__setattr__=dict.__setitem__;__delattr__=dict.__delitem__
def sparta_d015b3a1e7(appViewsModels):
	A=appViewsModels
	if isinstance(A,list):
		for C in A:
			for B in list(C.keys()):
				if isinstance(C[B],date):C[B]=str(C[B])
	else:
		for B in list(A.keys()):
			if isinstance(A[B],date):A[B]=str(A[B])
	return A
def sparta_8ec1a58679(thisText):A=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));A=A+str('/log/log.txt');B=open(A,'a');B.write(thisText);B.writelines('\n');B.close()
def sparta_1739123101(request):A=request;return{'appName':'Project','user':A.user,'ip_address':A.META['REMOTE_ADDR']}
def sparta_9faa96b2c6():return conf_settings.PLATFORM
def sparta_bfdefaa8a9():
	A=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));A=os.path.dirname(os.path.dirname(A))
	if conf_settings.DEBUG:C='static'
	else:C='staticfiles'
	E=A+f"/{C}/dist/manifest.json";F=open(E);B=json.load(F)
	if conf_settings.B_TOOLBAR:
		G=list(B.keys())
		for D in G:B[D]=A+f"/{C}"+B[D]
	return B
def sparta_5554065f87(request):
	B='';C=''
	if len(B)>0:B='/'+str(B)
	if len(C)>0:C='/'+str(C)
	F=sparta_e9605efc3e()
	try:
		A=_B;G=AppVersioning.objects.all();E=datetime.now().astimezone(UTC)
		if G.count()==0:AppVersioning.objects.create(last_check_date=E);A=_A
		else:
			D=G[0];I=D.last_check_date;J=E-I;K=D.last_available_version_pip
			if not F==K:A=_A
			elif J.seconds>60*10:A=_A;D.last_check_date=E;D.save()
	except:A=_A
	try:
		L=sparta_638705750a()['api']
		with open(os.path.join(L,'app_data_asgi.json'),'r')as M:N=json.load(M)
		H=int(N['default_port'])
	except:H=5664
	O=conf_settings.HOST_WS_PREFIX;P=conf_settings.WEBSOCKET_PREFIX;Q={'PROJECT_NAME':conf_settings.PROJECT_NAME,'IS_DEV_VIEW_ENABLED':conf_settings.IS_DEV_VIEW_ENABLED,'CAPTCHA_SITEKEY':conf_settings.CAPTCHA_SITEKEY,'WEBSOCKET_PREFIX':P,'URL_PREFIX':B,'URL_WS_PREFIX':C,'ASGI_PORT':H,'HOST_WS_PREFIX':O,'CHECK_VERSIONING':A,'CURRENT_VERSION':F,'IS_VITE':conf_settings.IS_VITE,'IS_DEV':conf_settings.IS_DEV,'IS_DOCKER':os.getenv('IS_REMOTE_SPARTAQUBE_CONTAINER','False')=='True'};return Q
def sparta_924e2e523b(captcha):
	D='errorMsg';B='res';A=captcha
	try:
		if A is not _C:
			if len(A)>0:
				E=sparta_41cb52c24c()['CAPTCHA_SECRET_KEY'];F=f"https://www.google.com/recaptcha/api/siteverify?secret={E}&response={A}";C=requests.get(F)
				if int(C.status_code)==200:
					G=json.loads(C.text)
					if G['success']:return{B:1}
	except Exception as H:return{B:-1,D:str(H)}
	return{B:-1,D:'Invalid captcha'}
def sparta_c40340748f(password):
	A=password;B=UserProfile.objects.filter(email=conf_settings.ADMIN_DEFAULT_EMAIL).all()
	if B.count()==0:return conf_settings.ADMIN_DEFAULT==A
	else:C=B[0];D=C.user;return D.check_password(A)
def sparta_e1972d2a19(code):
	A=code
	try:
		if A is not _C:
			if len(A)>0:
				B=os.getenv('SPARTAQUBE_PASSWORD','admin')
				if B==A:return _A
	except:return _B
	return _B
def sparta_0f86a5807b(user):
	F='default';A=dict()
	if not user.is_anonymous:
		E=UserProfile.objects.filter(user=user)
		if E.count()>0:
			B=E[0];D=B.avatar
			if D is not _C:D=B.avatar.avatar
			A['avatar']=D;A['userProfile']=B;C=B.editor_theme
			if C is _C:C=F
			elif len(C)==0:C=F
			else:C=B.editor_theme
			A['theme']=C;A['font_size']=B.font_size;A['B_DARK_THEME']=B.is_dark_theme;A['is_size_reduced_plot_db']=B.is_size_reduced_plot_db;A['is_size_reduced_api']=B.is_size_reduced_api
	A[_D]=sparta_bfdefaa8a9();return A
def sparta_72aacfc01f(user):A=dict();A[_D]=sparta_bfdefaa8a9();return A
def sparta_a708ad3a08():
	try:socket.create_connection(('1.1.1.1',53));return _A
	except OSError:pass
	return _B
def sparta_3afd25f68d():A=socket.gethostname();B=socket.gethostbyname(A);return A,B