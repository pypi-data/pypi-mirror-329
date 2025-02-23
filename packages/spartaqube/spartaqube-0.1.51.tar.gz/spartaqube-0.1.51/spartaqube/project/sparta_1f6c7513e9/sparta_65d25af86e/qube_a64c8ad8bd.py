_D='bCodeMirror'
_C='menuBar'
_B='windows'
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_3c031cc253.sparta_8fd6b56ef0.qube_d80062ebbf as qube_d80062ebbf
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff.qube_0e0a02b9a2 import sparta_5b0a6b77e6
from project.sparta_ab7a1c0e2d.sparta_6016211a05 import qube_98ebf6e674 as qube_98ebf6e674
from project.sparta_ab7a1c0e2d.sparta_3d65dcb7bc import qube_3092ed132a as qube_3092ed132a
def sparta_40fbb95963():
	A=platform.system()
	if A=='Windows':return _B
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_5b0a6b77e6
@login_required(redirect_field_name='login')
def sparta_6a49fa94a9(request):
	C=request;D=C.GET.get('edit')
	if D is None:D='-1'
	A=qube_d80062ebbf.sparta_5554065f87(C);A[_C]=9;F=qube_d80062ebbf.sparta_0f86a5807b(C.user);A.update(F);A[_D]=_A;A['edit_chart_id']=D
	def G(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	E=sparta_40fbb95963()
	if E==_B:B=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\dashboard"
	elif E=='linux':B=os.path.expanduser('~/SpartaQube/dashboard')
	elif E=='mac':B=os.path.expanduser('~/Library/Application Support\\SpartaQube\\dashboard')
	G(B);A['default_project_path']=B;print(f"default_project_path {B}");return render(C,'dist/project/dashboard/dashboard.html',A)
@csrf_exempt
def sparta_ffdf80fefa(request,id):
	A=request
	if id is None:B=A.GET.get('id')
	else:B=id
	return sparta_1be992fff7(A,B)
def sparta_1be992fff7(request,dashboard_id,session='-1'):
	G='res';E=dashboard_id;B=request;C=False
	if E is None:C=_A
	else:
		D=qube_3092ed132a.has_dashboard_access(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_6a49fa94a9(B)
	A=qube_d80062ebbf.sparta_5554065f87(B);A[_C]=9;I=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(I);A[_D]=_A;F=D['dashboard_obj'];A['b_require_password']=0 if D[G]==1 else 1;A['dashboard_id']=F.dashboard_id;A['dashboard_name']=F.name;A['bPublicUser']=B.user.is_anonymous;A['session']=str(session);return render(B,'dist/project/dashboard/dashboardRun.html',A)