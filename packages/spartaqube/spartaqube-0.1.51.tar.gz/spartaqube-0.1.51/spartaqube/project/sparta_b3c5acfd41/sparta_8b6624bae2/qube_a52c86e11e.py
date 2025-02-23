_I='error.txt'
_H='zipName'
_G='utf-8'
_F='attachment; filename={0}'
_E='appId'
_D='Content-Disposition'
_C='res'
_B='projectPath'
_A='jsonData'
import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_ab7a1c0e2d.sparta_1c4ec0e5b5 import qube_1fe7fcee70 as qube_1fe7fcee70
from project.sparta_ab7a1c0e2d.sparta_1c4ec0e5b5 import qube_cf9856289f as qube_cf9856289f
from project.sparta_ab7a1c0e2d.sparta_4fc6cad494 import qube_01c35b57ea as qube_01c35b57ea
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff.qube_0e0a02b9a2 import sparta_22afa6a0c1
@csrf_exempt
@sparta_22afa6a0c1
def sparta_fbeb6b32e5(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_1fe7fcee70.sparta_bf45785993(E,A.user,B[D])
	else:C={_C:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_5138557c06(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1fe7fcee70.sparta_824595e57c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_7eea0f701f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1fe7fcee70.sparta_42c2aa8809(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_064fbbdfc8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1fe7fcee70.sparta_4325e9e774(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_ef8ed24321(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cf9856289f.sparta_b71b9cd272(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_14116d47f2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1fe7fcee70.sparta_580e1f45ea(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_750312920d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1fe7fcee70.sparta_8eb6903dc3(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_68276bfe5e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1fe7fcee70.sparta_71769166b5(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_8ca25b37ac(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1fe7fcee70.sparta_a7d161e62f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_d397fc7eaa(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_1fe7fcee70.sparta_6fc3b39e5f(J,A.user)
	if C[_C]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_D]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_22afa6a0c1
def sparta_befe6aa3bb(request):
	E='folderName';C=request;F=C.GET[_B];D=C.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};B=qube_1fe7fcee70.sparta_5261055ac6(G,C.user);print(_C);print(B)
	if B[_C]==1:H=B['zip'];I=B[_H];A=HttpResponse();A.write(H.getvalue());A[_D]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_D]=_F.format(K)
	return A
@csrf_exempt
@sparta_22afa6a0c1
def sparta_bb33fed05e(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_1fe7fcee70.sparta_5d42a250cf(F,B.user)
	if C[_C]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_D]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_D]=_F.format(J)
	return A