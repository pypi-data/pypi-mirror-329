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
import project.sparta_8da3d59761.sparta_e1d65002c1.qube_87c1dfb7e8 as qube_87c1dfb7e8
from project.sparta_0c8b5020ad.sparta_c704a8bec8.qube_8bc7be3e5f import sparta_b83c31242b
from project.sparta_0c8b5020ad.sparta_87e47ed0f0 import qube_40c1566c0a as qube_40c1566c0a
from project.sparta_0c8b5020ad.sparta_7e6dd3e7f6 import qube_755b406e85 as qube_755b406e85
def sparta_7e22b2c145():
	A=platform.system()
	if A=='Windows':return _A
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_b83c31242b
@login_required(redirect_field_name='login')
def sparta_adabfbf3c2(request):A=request;B=qube_87c1dfb7e8.sparta_2dd044b9fe(A);B[_B]=-1;C=qube_87c1dfb7e8.sparta_cb8781f955(A.user);B.update(C);return render(A,'dist/project/homepage/homepage.html',B)
@csrf_exempt
@sparta_b83c31242b
@login_required(redirect_field_name='login')
def sparta_7f79c5a4ff(request,kernel_manager_uuid):
	E=kernel_manager_uuid;D=True;B=request;F=False
	if E is None:F=D
	else:
		G=qube_40c1566c0a.sparta_8d78924390(B.user,E)
		if G is None:F=D
	if F:return sparta_adabfbf3c2(B)
	def I(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=D)
	H=sparta_7e22b2c145()
	if H==_A:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\kernel"
	elif H=='linux':C=os.path.expanduser('~/SpartaQube/kernel')
	elif H=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\kernel')
	I(C);J=os.path.join(C,E);I(J);K=os.path.join(J,'main.ipynb')
	if not os.path.exists(K):
		L=qube_755b406e85.sparta_5c0448661b()
		with open(K,'w')as M:M.write(json.dumps(L))
	A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);A['default_project_path']=C;A[_B]=-1;N=qube_87c1dfb7e8.sparta_cb8781f955(B.user);A.update(N);A['kernel_name']=G.name;A['kernelManagerUUID']=G.kernel_manager_uuid;A['bCodeMirror']=D;A['bPublicUser']=B.user.is_anonymous;return render(B,'dist/project/sqKernelNotebook/sqKernelNotebook.html',A)