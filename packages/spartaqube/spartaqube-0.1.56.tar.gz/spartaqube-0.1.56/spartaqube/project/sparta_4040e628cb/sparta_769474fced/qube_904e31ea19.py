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
import project.sparta_3500f2f8a8.sparta_c6eb62a0d0.qube_0ad4e25f38 as qube_0ad4e25f38
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_f93fd87579
from project.sparta_662ef67a08.sparta_82d8bf2424 import qube_13c23816a0 as qube_13c23816a0
def sparta_a93cc5ef0f():
	A=platform.system()
	if A=='Windows':return _H
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_f93fd87579
@login_required(redirect_field_name='login')
def sparta_344160048c(request):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_0ad4e25f38.sparta_1ab7a89a58(B);return render(B,_D,A)
	qube_13c23816a0.sparta_be1c3c44aa();A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A[_E]=12;E=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(E);A[_F]=_A
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	D=sparta_a93cc5ef0f()
	if D==_H:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\developer"
	elif D=='linux':C=os.path.expanduser('~/SpartaQube/developer')
	elif D=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\developer')
	F(C);A[_G]=C;return render(B,'dist/project/developer/developer.html',A)
@csrf_exempt
def sparta_5afe52a1eb(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_0ad4e25f38.sparta_1ab7a89a58(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_13c23816a0.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_344160048c(B)
	A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A[_E]=12;H=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(H);A[_F]=_A;F=E[_I];A[_G]=F.project_path;A[_J]=0 if E[_C]==1 else 1;A[_K]=F.developer_id;A[_L]=F.name;A[_M]=B.user.is_anonymous;return render(B,'dist/project/developer/developerRun.html',A)
@csrf_exempt
@sparta_f93fd87579
@login_required(redirect_field_name='login')
def sparta_32825e78d1(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_0ad4e25f38.sparta_1ab7a89a58(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_13c23816a0.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_344160048c(B)
	A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A[_E]=12;H=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(H);A[_F]=_A;F=E[_I];A[_G]=F.project_path;A[_J]=0 if E[_C]==1 else 1;A[_K]=F.developer_id;A[_L]=F.name;A[_M]=B.user.is_anonymous;return render(B,'dist/project/developer/developerDetached.html',A)
def sparta_a3d2f1e200(request,project_path,file_name):A=project_path;A=unquote(A);return serve(request,file_name,document_root=A)