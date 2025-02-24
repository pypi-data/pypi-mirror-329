_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_0c8b5020ad.sparta_c704a8bec8 import qube_8bc7be3e5f as qube_8bc7be3e5f
from project.sparta_8da3d59761.sparta_e1d65002c1.qube_87c1dfb7e8 import sparta_282c550a19
from project.logger_config import logger
@csrf_exempt
def sparta_55966fc13d(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_8bc7be3e5f.sparta_55966fc13d(B)
@csrf_exempt
def sparta_56ca9bc89a(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_62f262d0fd(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_54426811eb(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)