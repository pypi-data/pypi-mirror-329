_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff import qube_0e0a02b9a2 as qube_0e0a02b9a2
from project.sparta_3c031cc253.sparta_8fd6b56ef0.qube_d80062ebbf import sparta_924e2e523b
@csrf_exempt
def sparta_0606a7cae6(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_0e0a02b9a2.sparta_0606a7cae6(B)
@csrf_exempt
def sparta_0666450832(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_9cbcf8c53b(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_398b96f2db(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)