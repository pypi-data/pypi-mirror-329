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
from project.sparta_ab7a1c0e2d.sparta_6d771044fa import qube_be81be5b57 as qube_be81be5b57
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff.qube_0e0a02b9a2 import sparta_22afa6a0c1
@csrf_exempt
@sparta_22afa6a0c1
def sparta_f6d45213cd(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_be81be5b57.sparta_f6d45213cd(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_f5b06dff7d(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_be81be5b57.sparta_f5b06dff7d(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_819f12eb69(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_be81be5b57.sparta_819f12eb69(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_8f8eb7df9e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_be81be5b57.sparta_8f8eb7df9e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_5d1d9460cb(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_be81be5b57.sparta_5d1d9460cb(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_9e57af9d13(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_be81be5b57.sparta_9e57af9d13(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_f99df2b233(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_be81be5b57.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_3f1a05dd56(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_be81be5b57.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_cfaaed348b(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_be81be5b57.sparta_cfaaed348b(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_1c9bccd360(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_be81be5b57.sparta_1c9bccd360(A,C);E=json.dumps(D);return HttpResponse(E)