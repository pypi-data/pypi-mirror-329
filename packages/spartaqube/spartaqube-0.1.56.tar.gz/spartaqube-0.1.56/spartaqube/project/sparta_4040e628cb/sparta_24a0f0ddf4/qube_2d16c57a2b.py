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
import project.sparta_3500f2f8a8.sparta_c6eb62a0d0.qube_0ad4e25f38 as qube_0ad4e25f38
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_f93fd87579
from project.sparta_662ef67a08.sparta_67a87b7baa import qube_a9e41d69b1 as qube_a9e41d69b1
def sparta_a93cc5ef0f():
	A=platform.system()
	if A=='Windows':return _G
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_f93fd87579
@login_required(redirect_field_name='login')
def sparta_212c326ce6(request):
	C=request;A=qube_0ad4e25f38.sparta_1ab7a89a58(C);A[_D]=13;E=qube_0ad4e25f38.sparta_e08ad78749(C.user);A.update(E);A[_E]=_A
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	D=sparta_a93cc5ef0f()
	if D==_G:B=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\notebook"
	elif D=='linux':B=os.path.expanduser('~/SpartaQube/notebook')
	elif D=='mac':B=os.path.expanduser('~/Library/Application Support\\SpartaQube\\notebook')
	F(B);A[_F]=B;return render(C,'dist/project/notebook/notebook.html',A)
@csrf_exempt
def sparta_ab4f21f18a(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_a9e41d69b1.sparta_8adc640bdf(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_212c326ce6(B)
	A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A[_D]=12;H=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(H);A[_E]=_A;F=E[_H];A[_F]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.notebook_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookRun.html',A)
@csrf_exempt
@sparta_f93fd87579
@login_required(redirect_field_name='login')
def sparta_385cf0d2c0(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_a9e41d69b1.sparta_8adc640bdf(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_212c326ce6(B)
	A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A[_D]=12;H=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(H);A[_E]=_A;F=E[_H];A[_F]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.notebook_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookDetached.html',A)