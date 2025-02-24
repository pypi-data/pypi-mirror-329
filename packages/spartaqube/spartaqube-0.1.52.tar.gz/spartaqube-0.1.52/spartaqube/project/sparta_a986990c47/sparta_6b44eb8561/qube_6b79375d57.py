_A='jsonData'
import json,inspect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from project.sparta_0c8b5020ad.sparta_5beab5dd83 import qube_f12f99a4ad as qube_f12f99a4ad
from project.sparta_0c8b5020ad.sparta_c704a8bec8.qube_8bc7be3e5f import sparta_3e75bbbf32
@csrf_exempt
@sparta_3e75bbbf32
def sparta_7b75fb208a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f12f99a4ad.sparta_7b75fb208a(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_5766289990(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_f12f99a4ad.sparta_5766289990(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_036b5c561a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_f12f99a4ad.sparta_036b5c561a(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_4f9f042ea3(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f12f99a4ad.sparta_4f9f042ea3(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_383da3551a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f12f99a4ad.sparta_383da3551a(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_c43c458e18(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f12f99a4ad.sparta_c43c458e18(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_89f94417f3(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_f12f99a4ad.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_6822fae6df(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f12f99a4ad.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_896ed63acf(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_f12f99a4ad.sparta_896ed63acf(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_ea1397616b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f12f99a4ad.sparta_ea1397616b(A,C);E=json.dumps(D);return HttpResponse(E)