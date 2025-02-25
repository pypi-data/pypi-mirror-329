_E='Content-Disposition'
_D='utf-8'
_C='dashboardId'
_B='projectPath'
_A='jsonData'
import os,json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_662ef67a08.sparta_130739942b import qube_fc5bfd1d02 as qube_fc5bfd1d02
from project.sparta_662ef67a08.sparta_130739942b import qube_67beb97de2 as qube_67beb97de2
from project.sparta_662ef67a08.sparta_9caf5c932d import qube_8d35301237 as qube_8d35301237
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_0d16fbb533,sparta_6c20046a0d
@csrf_exempt
def sparta_604cf10c80(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fc5bfd1d02.sparta_604cf10c80(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_82e23cd30e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fc5bfd1d02.sparta_82e23cd30e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_e8b10bf009(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fc5bfd1d02.sparta_e8b10bf009(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_c7028f0ca3(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fc5bfd1d02.sparta_c7028f0ca3(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_e051c58232(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fc5bfd1d02.sparta_e051c58232(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_622a93c394(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fc5bfd1d02.sparta_622a93c394(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_e0ba32d632(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fc5bfd1d02.sparta_e0ba32d632(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_665de7ef34(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fc5bfd1d02.sparta_665de7ef34(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_5696b7a638(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fc5bfd1d02.sparta_5696b7a638(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_74cbe63e06(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fc5bfd1d02.sparta_74cbe63e06(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_d4459a22f3(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_fc5bfd1d02.dashboard_project_explorer_delete_multiple_resources(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_6ee018c384(request):A=request;B=A.POST.dict();C=A.FILES;D=qube_fc5bfd1d02.sparta_6ee018c384(B,A.user,C['files[]']);E=json.dumps(D);return HttpResponse(E)
def sparta_3fd59aa394(path):
	A=path;A=os.path.normpath(A)
	if os.path.isfile(A):A=os.path.dirname(A)
	return os.path.basename(A)
def sparta_4020b039d0(path):A=path;A=os.path.normpath(A);return os.path.basename(A)
@csrf_exempt
@sparta_0d16fbb533
def sparta_3d8b6d674c(request):
	E='pathResource';A=request;B=A.GET[E];B=base64.b64decode(B).decode(_D);F=A.GET[_B];G=A.GET[_C];H=sparta_4020b039d0(B);I={E:B,_C:G,_B:base64.b64decode(F).decode(_D)};C=qube_fc5bfd1d02.sparta_2f301d65c4(I,A.user)
	if C['res']==1:
		try:
			with open(C['fullPath'],'rb')as J:D=HttpResponse(J.read(),content_type='application/force-download');D[_E]='attachment; filename='+str(H);return D
		except Exception as K:pass
	raise Http404
@csrf_exempt
@sparta_0d16fbb533
def sparta_1e4198a844(request):
	D='attachment; filename={0}';B=request;E=B.GET[_C];F=B.GET[_B];G={_C:E,_B:base64.b64decode(F).decode(_D)};C=qube_fc5bfd1d02.sparta_b49d65e9da(G,B.user)
	if C['res']==1:H=C['zip'];I=C['zipName'];A=HttpResponse();A.write(H.getvalue());A[_E]=D.format(f"{I}.zip")
	else:A=HttpResponse();J='Could not download the application, please try again';K='error.txt';A.write(J);A[_E]=D.format(K)
	return A
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_405691e897(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_67beb97de2.sparta_405691e897(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_6fe1b75816(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_67beb97de2.sparta_6fe1b75816(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_9ccb745db2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_67beb97de2.sparta_9ccb745db2(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_00f29a1f54(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_67beb97de2.sparta_00f29a1f54(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_dfe34b603b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_67beb97de2.sparta_dfe34b603b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_6bd4f5392c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_67beb97de2.sparta_6bd4f5392c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_6c69133c7f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_67beb97de2.sparta_6c69133c7f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_ae6538df5f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_67beb97de2.sparta_ae6538df5f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_fd68d5779f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_67beb97de2.sparta_fd68d5779f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_5fbc1e67ab(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_67beb97de2.sparta_5fbc1e67ab(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_1cf0df26c5(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_67beb97de2.sparta_1cf0df26c5(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_072c6ead97(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_67beb97de2.sparta_072c6ead97(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_e19e181cee(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_67beb97de2.sparta_e19e181cee(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
@sparta_6c20046a0d
def sparta_855a0cf615(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_67beb97de2.sparta_855a0cf615(C,A.user);E=json.dumps(D);return HttpResponse(E)