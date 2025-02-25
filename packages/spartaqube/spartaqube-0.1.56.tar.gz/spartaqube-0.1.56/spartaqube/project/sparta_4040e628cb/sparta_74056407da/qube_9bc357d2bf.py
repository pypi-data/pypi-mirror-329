_O='serialized_data'
_N='has_access'
_M='plot_name'
_L='plot_chart_id'
_K='dist/project/plot-db/plotDB.html'
_J='edit_chart_id'
_I='edit'
_H='plot_db_chart_obj'
_G=False
_F='login'
_E='-1'
_D='bCodeMirror'
_C='menuBar'
_B=None
_A=True
import json,base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_3500f2f8a8.sparta_c6eb62a0d0.qube_0ad4e25f38 as qube_0ad4e25f38
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_f93fd87579
from project.sparta_662ef67a08.sparta_928c4c5c7e import qube_8088811bba as qube_8088811bba
from project.sparta_662ef67a08.sparta_9caf5c932d import qube_8d35301237 as qube_8d35301237
@csrf_exempt
@sparta_f93fd87579
@login_required(redirect_field_name=_F)
def sparta_58152e93b8(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A[_C]=7;D=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_f93fd87579
@login_required(redirect_field_name=_F)
def sparta_72138a4cd0(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A[_C]=10;D=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_f93fd87579
@login_required(redirect_field_name=_F)
def sparta_53777f4d47(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A[_C]=11;D=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_f93fd87579
@login_required(redirect_field_name=_F)
def sparta_1c9e311ac4(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_8088811bba.sparta_56f380b76c(C,A.user);D=not E[_N]
	if D:return sparta_58152e93b8(A)
	B=qube_0ad4e25f38.sparta_1ab7a89a58(A);B[_C]=7;F=qube_0ad4e25f38.sparta_e08ad78749(A.user);B.update(F);B[_D]=_A;B[_L]=C;G=E[_H];B[_M]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_f93fd87579
def sparta_9db8ef3c1a(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return plot_widget_func(A,B)
@csrf_exempt
@sparta_f93fd87579
def sparta_f238c39aeb(request,dashboard_id,id,password):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	C=base64.b64decode(password).decode();return plot_widget_func(A,B,dashboard_id=dashboard_id,dashboard_password=C)
@csrf_exempt
@sparta_f93fd87579
def sparta_08ad547b3e(request,widget_id,session_id,api_token_id):return plot_widget_func(request,widget_id,session_id)
def plot_widget_func(request,plot_chart_id,session=_E,dashboard_id=_E,token_permission='',dashboard_password=_B):
	K='token_permission';I=dashboard_id;H=plot_chart_id;G='res';E=token_permission;D=request;C=_G
	if H is _B:C=_A
	else:
		B=qube_8088811bba.sparta_e89baab6c3(H,D.user);F=B[G]
		if F==-1:C=_A
	if C:
		if I!=_E:
			B=qube_8d35301237.has_plot_db_access(I,H,D.user,dashboard_password);F=B[G]
			if F==1:E=B[K];C=_G
	if C:
		if len(E)>0:
			B=qube_8088811bba.sparta_315f2a7987(E);F=B[G]
			if F==1:C=_G
	if C:return sparta_58152e93b8(D)
	A=qube_0ad4e25f38.sparta_1ab7a89a58(D);A[_C]=7;L=qube_0ad4e25f38.sparta_e08ad78749(D.user);A.update(L);A[_D]=_A;J=B[_H];A['b_require_password']=0 if B[G]==1 else 1;A[_L]=J.plot_chart_id;A[_M]=J.name;A['session']=str(session);A['is_dashboard_widget']=1 if I!=_E else 0;A['is_token']=1 if len(E)>0 else 0;A[K]=str(E);return render(D,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
def sparta_f79153107e(request,token):return plot_widget_func(request,plot_chart_id=_B,token_permission=token)
@csrf_exempt
@sparta_f93fd87579
def sparta_a8e5cb9e7d(request):B=request;A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A[_C]=7;C=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(C);A[_D]=_A;A[_O]=B.POST.get('data');return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_f93fd87579
@login_required(redirect_field_name=_F)
def sparta_213c1d4dc4(request,id):
	K=',\n    ';B=request;C=id;F=_G
	if C is _B:F=_A
	else:G=qube_8088811bba.sparta_56f380b76c(C,B.user);F=not G[_N]
	if F:return sparta_58152e93b8(B)
	L=qube_8088811bba.sparta_1f53efe345(G[_H]);D='';H=0
	for(E,I)in L.items():
		if H>0:D+=K
		if I==1:D+=f"{E}=input_{E}"
		else:M=str(K.join([f"input_{E}_{A}"for A in range(I)]));D+=f"{E}=[{M}]"
		H+=1
	J=f"'{C}'";N=f"\n    {J}\n";O=f"Spartaqube().get_widget({N})";P=f"\n    {J},\n    {D}\n";Q=f"Spartaqube().plot({P})";A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A[_C]=7;R=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(R);A[_D]=_A;A[_L]=C;S=G[_H];A[_M]=S.name;A['plot_data_cmd']=O;A['plot_data_cmd_inputs']=Q;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_f93fd87579
def sparta_6c658a5e0d(request,json_vars_html):B=request;A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A[_C]=7;C=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(C);A[_D]=_A;A.update(json.loads(json_vars_html));A[_O]=B.POST.get('data');return render(B,'dist/project/plot-db/plotAPI.html',A)