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
import project.sparta_3c031cc253.sparta_8fd6b56ef0.qube_d80062ebbf as qube_d80062ebbf
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff.qube_0e0a02b9a2 import sparta_5b0a6b77e6
from project.sparta_ab7a1c0e2d.sparta_fc9a1b9aff import qube_2a0f3208a0 as qube_2a0f3208a0
def sparta_40fbb95963():
	A=platform.system()
	if A=='Windows':return _G
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_5b0a6b77e6
@login_required(redirect_field_name='login')
def sparta_9c73294e44(request):
	C=request;A=qube_d80062ebbf.sparta_5554065f87(C);A[_D]=13;E=qube_d80062ebbf.sparta_0f86a5807b(C.user);A.update(E);A[_E]=_A
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	D=sparta_40fbb95963()
	if D==_G:B=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\notebook"
	elif D=='linux':B=os.path.expanduser('~/SpartaQube/notebook')
	elif D=='mac':B=os.path.expanduser('~/Library/Application Support\\SpartaQube\\notebook')
	F(B);A[_F]=B;print(f"default_project_path {B}");return render(C,'dist/project/notebook/notebook.html',A)
@csrf_exempt
def sparta_b914d751c1(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_2a0f3208a0.sparta_86672fd214(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_9c73294e44(B)
	A=qube_d80062ebbf.sparta_5554065f87(B);A[_D]=12;H=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(H);A[_E]=_A;F=E[_H];A[_F]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.notebook_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookRun.html',A)
@csrf_exempt
@sparta_5b0a6b77e6
@login_required(redirect_field_name='login')
def sparta_5b9bd6b344(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_2a0f3208a0.sparta_86672fd214(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_9c73294e44(B)
	A=qube_d80062ebbf.sparta_5554065f87(B);A[_D]=12;H=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(H);A[_E]=_A;F=E[_H];A[_F]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.notebook_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookDetached.html',A)