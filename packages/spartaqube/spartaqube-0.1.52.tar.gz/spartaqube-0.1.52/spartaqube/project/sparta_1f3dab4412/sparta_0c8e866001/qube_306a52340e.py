_D='bCodeMirror'
_C='menuBar'
_B='windows'
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_8da3d59761.sparta_e1d65002c1.qube_87c1dfb7e8 as qube_87c1dfb7e8
from project.sparta_0c8b5020ad.sparta_c704a8bec8.qube_8bc7be3e5f import sparta_b83c31242b
from project.sparta_0c8b5020ad.sparta_bf728a6b22 import qube_7f065f2f14 as qube_7f065f2f14
from project.sparta_0c8b5020ad.sparta_1aad359281 import qube_febb5b69bd as qube_febb5b69bd
def sparta_7e22b2c145():
	A=platform.system()
	if A=='Windows':return _B
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_b83c31242b
@login_required(redirect_field_name='login')
def sparta_2fc55953d4(request):
	B=request;D=B.GET.get('edit')
	if D is None:D='-1'
	A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);A[_C]=9;F=qube_87c1dfb7e8.sparta_cb8781f955(B.user);A.update(F);A[_D]=_A;A['edit_chart_id']=D
	def G(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	E=sparta_7e22b2c145()
	if E==_B:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\dashboard"
	elif E=='linux':C=os.path.expanduser('~/SpartaQube/dashboard')
	elif E=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\dashboard')
	G(C);A['default_project_path']=C;return render(B,'dist/project/dashboard/dashboard.html',A)
@csrf_exempt
def sparta_b4ae4cd58b(request,id):
	A=request
	if id is None:B=A.GET.get('id')
	else:B=id
	return sparta_df64e66f76(A,B)
def sparta_df64e66f76(request,dashboard_id,session='-1'):
	G='res';E=dashboard_id;B=request;C=False
	if E is None:C=_A
	else:
		D=qube_febb5b69bd.has_dashboard_access(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_2fc55953d4(B)
	A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);A[_C]=9;I=qube_87c1dfb7e8.sparta_cb8781f955(B.user);A.update(I);A[_D]=_A;F=D['dashboard_obj'];A['b_require_password']=0 if D[G]==1 else 1;A['dashboard_id']=F.dashboard_id;A['dashboard_name']=F.name;A['bPublicUser']=B.user.is_anonymous;A['session']=str(session);return render(B,'dist/project/dashboard/dashboardRun.html',A)