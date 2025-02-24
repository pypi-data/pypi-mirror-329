_L='bPublicUser'
_K='notebook_name'
_J='notebook_id'
_I='b_require_password'
_H='notebook_obj'
_G='windows'
_F='default_project_path'
_E='bCodeMirror'
_D='menuBar'
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
import project.sparta_8da3d59761.sparta_e1d65002c1.qube_87c1dfb7e8 as qube_87c1dfb7e8
from project.sparta_0c8b5020ad.sparta_c704a8bec8.qube_8bc7be3e5f import sparta_b83c31242b
from project.sparta_0c8b5020ad.sparta_da6d40a6fd import qube_fa876c1b25 as qube_fa876c1b25
def sparta_7e22b2c145():
	A=platform.system()
	if A=='Windows':return _G
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_b83c31242b
@login_required(redirect_field_name='login')
def sparta_7456ce6489(request):
	C=request;A=qube_87c1dfb7e8.sparta_2dd044b9fe(C);A[_D]=13;E=qube_87c1dfb7e8.sparta_cb8781f955(C.user);A.update(E);A[_E]=_A
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	D=sparta_7e22b2c145()
	if D==_G:B=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\notebook"
	elif D=='linux':B=os.path.expanduser('~/SpartaQube/notebook')
	elif D=='mac':B=os.path.expanduser('~/Library/Application Support\\SpartaQube\\notebook')
	F(B);A[_F]=B;return render(C,'dist/project/notebook/notebook.html',A)
@csrf_exempt
def sparta_04213bb65e(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_fa876c1b25.sparta_9d1a4eb1f2(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_7456ce6489(B)
	A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);A[_D]=12;H=qube_87c1dfb7e8.sparta_cb8781f955(B.user);A.update(H);A[_E]=_A;F=E[_H];A[_F]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.notebook_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookRun.html',A)
@csrf_exempt
@sparta_b83c31242b
@login_required(redirect_field_name='login')
def sparta_f1b205f9cf(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_fa876c1b25.sparta_9d1a4eb1f2(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_7456ce6489(B)
	A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);A[_D]=12;H=qube_87c1dfb7e8.sparta_cb8781f955(B.user);A.update(H);A[_E]=_A;F=E[_H];A[_F]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.notebook_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookDetached.html',A)