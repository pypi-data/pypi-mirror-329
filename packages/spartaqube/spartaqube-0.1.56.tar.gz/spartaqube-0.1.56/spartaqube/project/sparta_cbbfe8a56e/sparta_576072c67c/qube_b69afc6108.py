_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_662ef67a08.sparta_1616d6b2d2 import qube_381eed7f1c as qube_381eed7f1c
from project.sparta_3500f2f8a8.sparta_c6eb62a0d0.qube_0ad4e25f38 import sparta_2728fed9c6
from project.logger_config import logger
@csrf_exempt
def sparta_27448efe57(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_381eed7f1c.sparta_27448efe57(B)
@csrf_exempt
def sparta_ea6bfa4539(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_2a589b9daf(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_08ecd15992(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)