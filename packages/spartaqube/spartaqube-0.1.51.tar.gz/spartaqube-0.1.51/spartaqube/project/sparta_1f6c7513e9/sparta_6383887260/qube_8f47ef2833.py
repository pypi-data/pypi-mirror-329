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
import project.sparta_3c031cc253.sparta_8fd6b56ef0.qube_d80062ebbf as qube_d80062ebbf
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff.qube_0e0a02b9a2 import sparta_5b0a6b77e6
from project.sparta_ab7a1c0e2d.sparta_a0284b3272 import qube_c8c9fd3a9f as qube_c8c9fd3a9f
from project.sparta_ab7a1c0e2d.sparta_c744d29a89 import qube_7cb1e8e776 as qube_7cb1e8e776
def sparta_40fbb95963():
	A=platform.system()
	if A=='Windows':return _A
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_5b0a6b77e6
@login_required(redirect_field_name='login')
def sparta_a696ae8ab9(request):A=request;B=qube_d80062ebbf.sparta_5554065f87(A);B[_B]=-1;C=qube_d80062ebbf.sparta_0f86a5807b(A.user);B.update(C);return render(A,'dist/project/homepage/homepage.html',B)
@csrf_exempt
@sparta_5b0a6b77e6
@login_required(redirect_field_name='login')
def sparta_9c3444d5c6(request,kernel_manager_uuid):
	E=kernel_manager_uuid;D=True;B=request;F=False
	if E is None:F=D
	else:
		G=qube_c8c9fd3a9f.sparta_b187c89f8d(B.user,E)
		if G is None:F=D
	if F:return sparta_a696ae8ab9(B)
	def I(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=D)
	H=sparta_40fbb95963()
	if H==_A:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\kernel"
	elif H=='linux':C=os.path.expanduser('~/SpartaQube/kernel')
	elif H=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\kernel')
	I(C);J=os.path.join(C,E);I(J);K=os.path.join(J,'main.ipynb')
	if not os.path.exists(K):
		L=qube_7cb1e8e776.sparta_05024c3ff3()
		with open(K,'w')as M:M.write(json.dumps(L))
	A=qube_d80062ebbf.sparta_5554065f87(B);A['default_project_path']=C;A[_B]=-1;N=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(N);A['kernel_name']=G.name;A['kernelManagerUUID']=G.kernel_manager_uuid;A['bCodeMirror']=D;A['bPublicUser']=B.user.is_anonymous;return render(B,'dist/project/sqKernelNotebook/sqKernelNotebook.html',A)