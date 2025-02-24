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
from project.sparta_0c8b5020ad.sparta_f4e4c20261 import qube_6e053437bc as qube_6e053437bc
from project.sparta_0c8b5020ad.sparta_f4e4c20261 import qube_f928b960cf as qube_f928b960cf
from project.sparta_0c8b5020ad.sparta_2b5b2a60e0 import qube_979597c799 as qube_979597c799
from project.sparta_0c8b5020ad.sparta_c704a8bec8.qube_8bc7be3e5f import sparta_3e75bbbf32
@csrf_exempt
@sparta_3e75bbbf32
def sparta_7540164ee2(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_6e053437bc.sparta_d70e8a93e9(E,A.user,B[D])
	else:C={_D:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_339a7c9d55(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6e053437bc.sparta_08fb6081a8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_92a1756631(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6e053437bc.sparta_bea1f87f81(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_45dbc2aba9(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6e053437bc.sparta_6bbafbc929(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_9f61feeb7e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f928b960cf.sparta_d70dba05f1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_17225c2235(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6e053437bc.sparta_c7e7b4b2a4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_f1eaf9d5e2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6e053437bc.sparta_7fa930a0aa(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_f49c914d9b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6e053437bc.sparta_d0416c5882(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_5d7bb342d8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6e053437bc.sparta_732322eac6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_3e3433365d(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_6e053437bc.sparta_41e8b01b0e(J,A.user)
	if C[_D]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_C]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_3e75bbbf32
def sparta_24405c6094(request):
	E='folderName';B=request;F=B.GET[_B];D=B.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};C=qube_6e053437bc.sparta_40b22ee21c(G,B.user)
	if C[_D]==1:H=C['zip'];I=C[_H];A=HttpResponse();A.write(H.getvalue());A[_C]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_C]=_F.format(K)
	return A
@csrf_exempt
@sparta_3e75bbbf32
def sparta_276c590a74(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_6e053437bc.sparta_553c724f8d(F,B.user)
	if C[_D]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_C]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_C]=_F.format(J)
	return A