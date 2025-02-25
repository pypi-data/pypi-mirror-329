_I='error.txt'
_H='zipName'
_G='utf-8'
_F='attachment; filename={0}'
_E='appId'
_D='res'
_C='Content-Disposition'
_B='projectPath'
_A='jsonData'
import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_662ef67a08.sparta_580e10d089 import qube_cde2cb7c21 as qube_cde2cb7c21
from project.sparta_662ef67a08.sparta_580e10d089 import qube_0f6b5b06b1 as qube_0f6b5b06b1
from project.sparta_662ef67a08.sparta_bc02ea2c9b import qube_2ac5797abc as qube_2ac5797abc
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_0d16fbb533
@csrf_exempt
@sparta_0d16fbb533
def sparta_3b999071d5(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_cde2cb7c21.sparta_5578225f14(E,A.user,B[D])
	else:C={_D:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_0d16fbb533
def sparta_3b26845562(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cde2cb7c21.sparta_db45b04bb3(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_0cad059be5(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cde2cb7c21.sparta_3c87b622fa(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_768c6ca545(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cde2cb7c21.sparta_2dac6863a4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_a30eee3a28(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_0f6b5b06b1.sparta_faac48a387(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_a574c797a2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cde2cb7c21.sparta_481c7f2e74(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_4b77b46c67(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cde2cb7c21.sparta_37c41b0a7c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_5cbf852773(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cde2cb7c21.sparta_42d428e08b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_aa717c1bb0(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cde2cb7c21.sparta_528edf51e8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_d3447285fc(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_cde2cb7c21.sparta_2f301d65c4(J,A.user)
	if C[_D]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_C]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_0d16fbb533
def sparta_40f9ba9fa7(request):
	E='folderName';B=request;F=B.GET[_B];D=B.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};C=qube_cde2cb7c21.sparta_b711f966f0(G,B.user)
	if C[_D]==1:H=C['zip'];I=C[_H];A=HttpResponse();A.write(H.getvalue());A[_C]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_C]=_F.format(K)
	return A
@csrf_exempt
@sparta_0d16fbb533
def sparta_f351c6a4c1(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_cde2cb7c21.sparta_b49d65e9da(F,B.user)
	if C[_D]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_C]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_C]=_F.format(J)
	return A