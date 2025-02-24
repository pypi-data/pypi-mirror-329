_E='Content-Disposition'
_D='utf-8'
_C='dashboardId'
_B='projectPath'
_A='jsonData'
import os,json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_0c8b5020ad.sparta_7e6dd3e7f6 import qube_3c05f6cfa2 as qube_3c05f6cfa2
from project.sparta_0c8b5020ad.sparta_7e6dd3e7f6 import qube_9c7e3afdf0 as qube_9c7e3afdf0
from project.sparta_0c8b5020ad.sparta_1aad359281 import qube_febb5b69bd as qube_febb5b69bd
from project.sparta_0c8b5020ad.sparta_c704a8bec8.qube_8bc7be3e5f import sparta_3e75bbbf32,sparta_a64f436d97
@csrf_exempt
def sparta_e8aa6c93a5(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3c05f6cfa2.sparta_e8aa6c93a5(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_81364b4259(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3c05f6cfa2.sparta_81364b4259(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_caddce3522(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3c05f6cfa2.sparta_caddce3522(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_14ba926c5b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3c05f6cfa2.sparta_14ba926c5b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_55d17bd263(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3c05f6cfa2.sparta_55d17bd263(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_713d006be8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3c05f6cfa2.sparta_713d006be8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_48e61a67bc(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3c05f6cfa2.sparta_48e61a67bc(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_e127591408(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3c05f6cfa2.sparta_e127591408(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_afb335e4f1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3c05f6cfa2.sparta_afb335e4f1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_73a8aa73e5(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3c05f6cfa2.sparta_73a8aa73e5(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_02b4621c4c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3c05f6cfa2.dashboard_project_explorer_delete_multiple_resources(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_513389f208(request):A=request;B=A.POST.dict();C=A.FILES;D=qube_3c05f6cfa2.sparta_513389f208(B,A.user,C['files[]']);E=json.dumps(D);return HttpResponse(E)
def sparta_383253f9ee(path):
	A=path;A=os.path.normpath(A)
	if os.path.isfile(A):A=os.path.dirname(A)
	return os.path.basename(A)
def sparta_8ce7abf42b(path):A=path;A=os.path.normpath(A);return os.path.basename(A)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_45800719bc(request):
	E='pathResource';A=request;B=A.GET[E];B=base64.b64decode(B).decode(_D);F=A.GET[_B];G=A.GET[_C];H=sparta_8ce7abf42b(B);I={E:B,_C:G,_B:base64.b64decode(F).decode(_D)};C=qube_3c05f6cfa2.sparta_41e8b01b0e(I,A.user)
	if C['res']==1:
		try:
			with open(C['fullPath'],'rb')as J:D=HttpResponse(J.read(),content_type='application/force-download');D[_E]='attachment; filename='+str(H);return D
		except Exception as K:pass
	raise Http404
@csrf_exempt
@sparta_3e75bbbf32
def sparta_a872ef6f87(request):
	D='attachment; filename={0}';B=request;E=B.GET[_C];F=B.GET[_B];G={_C:E,_B:base64.b64decode(F).decode(_D)};C=qube_3c05f6cfa2.sparta_553c724f8d(G,B.user)
	if C['res']==1:H=C['zip'];I=C['zipName'];A=HttpResponse();A.write(H.getvalue());A[_E]=D.format(f"{I}.zip")
	else:A=HttpResponse();J='Could not download the application, please try again';K='error.txt';A.write(J);A[_E]=D.format(K)
	return A
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_faf4401641(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9c7e3afdf0.sparta_faf4401641(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_861ec7ffa8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9c7e3afdf0.sparta_861ec7ffa8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_6276917b8c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9c7e3afdf0.sparta_6276917b8c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_75a755bfc4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9c7e3afdf0.sparta_75a755bfc4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_bdb9650ba8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9c7e3afdf0.sparta_bdb9650ba8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_3822ce1447(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9c7e3afdf0.sparta_3822ce1447(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_6a04cfda57(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9c7e3afdf0.sparta_6a04cfda57(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_9ba6c9ded8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9c7e3afdf0.sparta_9ba6c9ded8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_fe2b14447c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9c7e3afdf0.sparta_fe2b14447c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_08378a2a83(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9c7e3afdf0.sparta_08378a2a83(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_c2499bf071(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9c7e3afdf0.sparta_c2499bf071(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_8d90f39302(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9c7e3afdf0.sparta_8d90f39302(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_ca2ffb2993(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9c7e3afdf0.sparta_ca2ffb2993(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
@sparta_a64f436d97
def sparta_271cdb279f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9c7e3afdf0.sparta_271cdb279f(C,A.user);E=json.dumps(D);return HttpResponse(E)