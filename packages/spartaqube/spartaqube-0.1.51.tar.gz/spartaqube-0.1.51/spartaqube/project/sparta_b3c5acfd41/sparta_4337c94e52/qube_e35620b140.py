_E='Content-Disposition'
_D='utf-8'
_C='dashboardId'
_B='projectPath'
_A='jsonData'
import os,json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_ab7a1c0e2d.sparta_c744d29a89 import qube_b65c8bd7b1 as qube_b65c8bd7b1
from project.sparta_ab7a1c0e2d.sparta_c744d29a89 import qube_d81e305624 as qube_d81e305624
from project.sparta_ab7a1c0e2d.sparta_3d65dcb7bc import qube_3092ed132a as qube_3092ed132a
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff.qube_0e0a02b9a2 import sparta_22afa6a0c1,sparta_7322343753
@csrf_exempt
def sparta_55bc25bce4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b65c8bd7b1.sparta_55bc25bce4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_db4debfaec(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b65c8bd7b1.sparta_db4debfaec(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_237685945c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b65c8bd7b1.sparta_237685945c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_3647643dbb(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b65c8bd7b1.sparta_3647643dbb(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_ad7263cd23(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b65c8bd7b1.sparta_ad7263cd23(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_2197c17c2d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b65c8bd7b1.sparta_2197c17c2d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_c9b8032611(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b65c8bd7b1.sparta_c9b8032611(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_b3b39b6c6c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b65c8bd7b1.sparta_b3b39b6c6c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_3c5e64bb98(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b65c8bd7b1.sparta_3c5e64bb98(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_96b27afe20(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b65c8bd7b1.sparta_96b27afe20(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_efa5dd3b27(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b65c8bd7b1.dashboard_project_explorer_delete_multiple_resources(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_89c95c906c(request):A=request;B=A.POST.dict();C=A.FILES;D=qube_b65c8bd7b1.sparta_89c95c906c(B,A.user,C['files[]']);E=json.dumps(D);return HttpResponse(E)
def sparta_13666152d3(path):
	A=path;A=os.path.normpath(A)
	if os.path.isfile(A):A=os.path.dirname(A)
	return os.path.basename(A)
def sparta_88c859f702(path):A=path;A=os.path.normpath(A);return os.path.basename(A)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_e0838af9ce(request):
	E='pathResource';A=request;B=A.GET[E];B=base64.b64decode(B).decode(_D);F=A.GET[_B];G=A.GET[_C];H=sparta_88c859f702(B);I={E:B,_C:G,_B:base64.b64decode(F).decode(_D)};C=qube_b65c8bd7b1.sparta_6fc3b39e5f(I,A.user)
	if C['res']==1:
		try:
			with open(C['fullPath'],'rb')as J:D=HttpResponse(J.read(),content_type='application/force-download');D[_E]='attachment; filename='+str(H);return D
		except Exception as K:pass
	raise Http404
@csrf_exempt
@sparta_22afa6a0c1
def sparta_e490254ecd(request):
	D='attachment; filename={0}';B=request;E=B.GET[_C];F=B.GET[_B];G={_C:E,_B:base64.b64decode(F).decode(_D)};C=qube_b65c8bd7b1.sparta_5d42a250cf(G,B.user)
	if C['res']==1:H=C['zip'];I=C['zipName'];A=HttpResponse();A.write(H.getvalue());A[_E]=D.format(f"{I}.zip")
	else:A=HttpResponse();J='Could not download the application, please try again';K='error.txt';A.write(J);A[_E]=D.format(K)
	return A
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_2d1a3b5550(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d81e305624.sparta_2d1a3b5550(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_a0f6d8d978(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d81e305624.sparta_a0f6d8d978(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_f24ff2685e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d81e305624.sparta_f24ff2685e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_12b9bbbb34(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d81e305624.sparta_12b9bbbb34(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_90f7677395(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d81e305624.sparta_90f7677395(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_38be4fa743(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d81e305624.sparta_38be4fa743(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_6bcf9ffc88(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d81e305624.sparta_6bcf9ffc88(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_9c9a0f8918(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d81e305624.sparta_9c9a0f8918(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_f158736c3e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d81e305624.sparta_f158736c3e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_a42ed51b7c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d81e305624.sparta_a42ed51b7c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_3c17824bbf(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d81e305624.sparta_3c17824bbf(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_3ca1b61aec(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d81e305624.sparta_3ca1b61aec(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_f9a5b588cb(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d81e305624.sparta_f9a5b588cb(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
@sparta_7322343753
def sparta_c6394a81fb(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d81e305624.sparta_c6394a81fb(C,A.user);E=json.dumps(D);return HttpResponse(E)