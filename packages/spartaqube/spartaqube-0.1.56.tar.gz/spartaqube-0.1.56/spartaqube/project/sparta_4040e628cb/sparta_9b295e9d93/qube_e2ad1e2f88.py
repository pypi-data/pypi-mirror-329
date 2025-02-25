_B='menuBar'
_A='windows'
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
from project.sparta_662ef67a08.sparta_054f72bfca import qube_c08e7e260b as qube_c08e7e260b
from project.sparta_662ef67a08.sparta_130739942b import qube_952fdf29a0 as qube_952fdf29a0
def sparta_a93cc5ef0f():
	A=platform.system()
	if A=='Windows':return _A
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_f93fd87579
@login_required(redirect_field_name='login')
def sparta_964bc2aa52(request):A=request;B=qube_0ad4e25f38.sparta_1ab7a89a58(A);B[_B]=-1;C=qube_0ad4e25f38.sparta_e08ad78749(A.user);B.update(C);return render(A,'dist/project/homepage/homepage.html',B)
@csrf_exempt
@sparta_f93fd87579
@login_required(redirect_field_name='login')
def sparta_29959cc103(request,kernel_manager_uuid):
	E=kernel_manager_uuid;D=True;B=request;F=False
	if E is None:F=D
	else:
		G=qube_c08e7e260b.sparta_3c3ce6af33(B.user,E)
		if G is None:F=D
	if F:return sparta_964bc2aa52(B)
	def I(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=D)
	H=sparta_a93cc5ef0f()
	if H==_A:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\kernel"
	elif H=='linux':C=os.path.expanduser('~/SpartaQube/kernel')
	elif H=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\kernel')
	I(C);J=os.path.join(C,E);I(J);K=os.path.join(J,'main.ipynb')
	if not os.path.exists(K):
		L=qube_952fdf29a0.sparta_3e22d58347()
		with open(K,'w')as M:M.write(json.dumps(L))
	A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A['default_project_path']=C;A[_B]=-1;N=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(N);A['kernel_name']=G.name;A['kernelManagerUUID']=G.kernel_manager_uuid;A['bCodeMirror']=D;A['bPublicUser']=B.user.is_anonymous;return render(B,'dist/project/sqKernelNotebook/sqKernelNotebook.html',A)