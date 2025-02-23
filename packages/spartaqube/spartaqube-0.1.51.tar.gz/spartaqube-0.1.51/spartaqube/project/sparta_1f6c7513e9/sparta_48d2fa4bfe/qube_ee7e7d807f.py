_M='bPublicUser'
_L='developer_name'
_K='developer_id'
_J='b_require_password'
_I='developer_obj'
_H='windows'
_G='default_project_path'
_F='bCodeMirror'
_E='menuBar'
_D='dist/project/homepage/homepage.html'
_C='res'
_B=None
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from django.http import FileResponse,Http404
from urllib.parse import unquote
from django.conf import settings as conf_settings
import project.sparta_3c031cc253.sparta_8fd6b56ef0.qube_d80062ebbf as qube_d80062ebbf
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff.qube_0e0a02b9a2 import sparta_5b0a6b77e6
from project.sparta_ab7a1c0e2d.sparta_9cfa7981a0 import qube_96f90e0ba5 as qube_96f90e0ba5
def sparta_40fbb95963():
	A=platform.system()
	if A=='Windows':return _H
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_5b0a6b77e6
@login_required(redirect_field_name='login')
def sparta_fc07739fef(request):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_d80062ebbf.sparta_5554065f87(B);return render(B,_D,A)
	qube_96f90e0ba5.sparta_7aa5fb26f3();A=qube_d80062ebbf.sparta_5554065f87(B);A[_E]=12;E=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(E);A[_F]=_A
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	D=sparta_40fbb95963()
	if D==_H:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\developer"
	elif D=='linux':C=os.path.expanduser('~/SpartaQube/developer')
	elif D=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\developer')
	F(C);A[_G]=C;print(f"default_project_path {C}");return render(B,'dist/project/developer/developer.html',A)
@csrf_exempt
def sparta_fc5769d594(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_d80062ebbf.sparta_5554065f87(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_96f90e0ba5.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_fc07739fef(B)
	A=qube_d80062ebbf.sparta_5554065f87(B);A[_E]=12;H=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(H);A[_F]=_A;F=E[_I];A[_G]=F.project_path;A[_J]=0 if E[_C]==1 else 1;A[_K]=F.developer_id;A[_L]=F.name;A[_M]=B.user.is_anonymous;return render(B,'dist/project/developer/developerRun.html',A)
@csrf_exempt
@sparta_5b0a6b77e6
@login_required(redirect_field_name='login')
def sparta_b6c6bcf7b3(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_d80062ebbf.sparta_5554065f87(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_96f90e0ba5.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_fc07739fef(B)
	A=qube_d80062ebbf.sparta_5554065f87(B);A[_E]=12;H=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(H);A[_F]=_A;F=E[_I];A[_G]=F.project_path;A[_J]=0 if E[_C]==1 else 1;A[_K]=F.developer_id;A[_L]=F.name;A[_M]=B.user.is_anonymous;return render(B,'dist/project/developer/developerDetached.html',A)
def sparta_54e0870ae6(request,project_path,file_name):C=file_name;B=request;A=project_path;print('request DEBUG');print(B);A=unquote(A);print(f"Serve {C} on project_path {A}");return serve(B,C,document_root=A)