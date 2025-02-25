_D='bCodeMirror'
_C='menuBar'
_B='windows'
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_3500f2f8a8.sparta_c6eb62a0d0.qube_0ad4e25f38 as qube_0ad4e25f38
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_f93fd87579
from project.sparta_662ef67a08.sparta_928c4c5c7e import qube_8088811bba as qube_8088811bba
from project.sparta_662ef67a08.sparta_9caf5c932d import qube_8d35301237 as qube_8d35301237
def sparta_a93cc5ef0f():
	A=platform.system()
	if A=='Windows':return _B
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_f93fd87579
@login_required(redirect_field_name='login')
def sparta_4c01cdeb05(request):
	B=request;D=B.GET.get('edit')
	if D is None:D='-1'
	A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A[_C]=9;F=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(F);A[_D]=_A;A['edit_chart_id']=D
	def G(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	E=sparta_a93cc5ef0f()
	if E==_B:C=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\dashboard"
	elif E=='linux':C=os.path.expanduser('~/SpartaQube/dashboard')
	elif E=='mac':C=os.path.expanduser('~/Library/Application Support\\SpartaQube\\dashboard')
	G(C);A['default_project_path']=C;return render(B,'dist/project/dashboard/dashboard.html',A)
@csrf_exempt
def sparta_35d40db26b(request,id):
	A=request
	if id is None:B=A.GET.get('id')
	else:B=id
	return sparta_89f5a2779e(A,B)
def sparta_89f5a2779e(request,dashboard_id,session='-1'):
	G='res';E=dashboard_id;B=request;C=False
	if E is None:C=_A
	else:
		D=qube_8d35301237.has_dashboard_access(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_4c01cdeb05(B)
	A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A[_C]=9;I=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(I);A[_D]=_A;F=D['dashboard_obj'];A['b_require_password']=0 if D[G]==1 else 1;A['dashboard_id']=F.dashboard_id;A['dashboard_name']=F.name;A['bPublicUser']=B.user.is_anonymous;A['session']=str(session);return render(B,'dist/project/dashboard/dashboardRun.html',A)