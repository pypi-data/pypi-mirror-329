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
import project.sparta_3c031cc253.sparta_8fd6b56ef0.qube_d80062ebbf as qube_d80062ebbf
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff.qube_0e0a02b9a2 import sparta_5b0a6b77e6
from project.sparta_ab7a1c0e2d.sparta_6016211a05 import qube_98ebf6e674 as qube_98ebf6e674
from project.sparta_ab7a1c0e2d.sparta_3d65dcb7bc import qube_3092ed132a as qube_3092ed132a
@csrf_exempt
@sparta_5b0a6b77e6
@login_required(redirect_field_name=_F)
def sparta_dc3c0a698c(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_d80062ebbf.sparta_5554065f87(B);A[_C]=7;D=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_5b0a6b77e6
@login_required(redirect_field_name=_F)
def sparta_a7e9d3cc96(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_d80062ebbf.sparta_5554065f87(B);A[_C]=10;D=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_5b0a6b77e6
@login_required(redirect_field_name=_F)
def sparta_287b408dc0(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_d80062ebbf.sparta_5554065f87(B);A[_C]=11;D=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_5b0a6b77e6
@login_required(redirect_field_name=_F)
def sparta_46d752cb6b(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_98ebf6e674.sparta_9a7eed9d87(C,A.user);D=not E[_N]
	if D:return sparta_dc3c0a698c(A)
	B=qube_d80062ebbf.sparta_5554065f87(A);B[_C]=7;F=qube_d80062ebbf.sparta_0f86a5807b(A.user);B.update(F);B[_D]=_A;B[_L]=C;G=E[_H];B[_M]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_5b0a6b77e6
def sparta_07b88b6b7e(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return plot_widget_func(A,B)
@csrf_exempt
@sparta_5b0a6b77e6
def sparta_d62591f785(request,dashboard_id,id,password):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	C=base64.b64decode(password).decode();return plot_widget_func(A,B,dashboard_id=dashboard_id,dashboard_password=C)
@csrf_exempt
@sparta_5b0a6b77e6
def sparta_7248f2d76c(request,widget_id,session_id,api_token_id):return plot_widget_func(request,widget_id,session_id)
def plot_widget_func(request,plot_chart_id,session=_E,dashboard_id=_E,token_permission='',dashboard_password=_B):
	K='token_permission';I=dashboard_id;H=plot_chart_id;G='res';E=token_permission;D=request;C=_G
	if H is _B:C=_A
	else:
		B=qube_98ebf6e674.sparta_00bf40d847(H,D.user);F=B[G]
		if F==-1:C=_A
	if C:
		if I!=_E:
			B=qube_3092ed132a.has_plot_db_access(I,H,D.user,dashboard_password);F=B[G]
			if F==1:E=B[K];C=_G
	if C:
		if len(E)>0:
			B=qube_98ebf6e674.sparta_8865c14437(E);F=B[G]
			if F==1:C=_G
	if C:return sparta_dc3c0a698c(D)
	A=qube_d80062ebbf.sparta_5554065f87(D);A[_C]=7;L=qube_d80062ebbf.sparta_0f86a5807b(D.user);A.update(L);A[_D]=_A;J=B[_H];A['b_require_password']=0 if B[G]==1 else 1;A[_L]=J.plot_chart_id;A[_M]=J.name;A['session']=str(session);A['is_dashboard_widget']=1 if I!=_E else 0;A['is_token']=1 if len(E)>0 else 0;A[K]=str(E);return render(D,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
def sparta_b0da10b558(request,token):return plot_widget_func(request,plot_chart_id=_B,token_permission=token)
@csrf_exempt
@sparta_5b0a6b77e6
def sparta_d0acee9934(request):B=request;A=qube_d80062ebbf.sparta_5554065f87(B);A[_C]=7;C=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(C);A[_D]=_A;A[_O]=B.POST.get('data');return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_5b0a6b77e6
@login_required(redirect_field_name=_F)
def sparta_a82177e5f8(request,id):
	K=',\n    ';B=request;C=id;F=_G
	if C is _B:F=_A
	else:G=qube_98ebf6e674.sparta_9a7eed9d87(C,B.user);F=not G[_N]
	if F:return sparta_dc3c0a698c(B)
	L=qube_98ebf6e674.sparta_836efa5885(G[_H]);D='';H=0
	for(E,I)in L.items():
		if H>0:D+=K
		if I==1:D+=f"{E}=input_{E}"
		else:M=str(K.join([f"input_{E}_{A}"for A in range(I)]));D+=f"{E}=[{M}]"
		H+=1
	J=f"'{C}'";N=f"\n    {J}\n";O=f"Spartaqube().get_widget({N})";P=f"\n    {J},\n    {D}\n";Q=f"Spartaqube().plot({P})";A=qube_d80062ebbf.sparta_5554065f87(B);A[_C]=7;R=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(R);A[_D]=_A;A[_L]=C;S=G[_H];A[_M]=S.name;A['plot_data_cmd']=O;A['plot_data_cmd_inputs']=Q;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_5b0a6b77e6
def sparta_ab36ffb5b8(request,json_vars_html):B=request;A=qube_d80062ebbf.sparta_5554065f87(B);A[_C]=7;C=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(C);A[_D]=_A;A.update(json.loads(json_vars_html));A[_O]=B.POST.get('data');return render(B,'dist/project/plot-db/plotAPI.html',A)