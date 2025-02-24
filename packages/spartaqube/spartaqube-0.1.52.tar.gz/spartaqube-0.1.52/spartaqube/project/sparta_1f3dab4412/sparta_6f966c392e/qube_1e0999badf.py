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
import project.sparta_8da3d59761.sparta_e1d65002c1.qube_87c1dfb7e8 as qube_87c1dfb7e8
from project.sparta_0c8b5020ad.sparta_c704a8bec8.qube_8bc7be3e5f import sparta_b83c31242b
from project.sparta_0c8b5020ad.sparta_76235df4f8 import qube_24d3483d51 as qube_24d3483d51
def sparta_7e22b2c145():
	A=platform.system()
	if A=='Windows':return _H
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_b83c31242b
@login_required(redirect_field_name='login')
def sparta_184e481ab8(request):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);return render(B,_D,A)
	qube_24d3483d51.sparta_9b156b0c32();A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);A[_E]=12;E=qube_87c1dfb7e8.sparta_cb8781f955(B.user);A.update(E);A[_F]=_A
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	D=sparta_7e22b2c145()
	if D==_H:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\developer"
	elif D=='linux':C=os.path.expanduser('~/SpartaQube/developer')
	elif D=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\developer')
	F(C);A[_G]=C;return render(B,'dist/project/developer/developer.html',A)
@csrf_exempt
def sparta_2c2c5e81b0(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_24d3483d51.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_184e481ab8(B)
	A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);A[_E]=12;H=qube_87c1dfb7e8.sparta_cb8781f955(B.user);A.update(H);A[_F]=_A;F=E[_I];A[_G]=F.project_path;A[_J]=0 if E[_C]==1 else 1;A[_K]=F.developer_id;A[_L]=F.name;A[_M]=B.user.is_anonymous;return render(B,'dist/project/developer/developerRun.html',A)
@csrf_exempt
@sparta_b83c31242b
@login_required(redirect_field_name='login')
def sparta_dc3ba87a31(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_24d3483d51.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_184e481ab8(B)
	A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);A[_E]=12;H=qube_87c1dfb7e8.sparta_cb8781f955(B.user);A.update(H);A[_F]=_A;F=E[_I];A[_G]=F.project_path;A[_J]=0 if E[_C]==1 else 1;A[_K]=F.developer_id;A[_L]=F.name;A[_M]=B.user.is_anonymous;return render(B,'dist/project/developer/developerDetached.html',A)
def sparta_eeb2dd47da(request,project_path,file_name):A=project_path;A=unquote(A);return serve(request,file_name,document_root=A)