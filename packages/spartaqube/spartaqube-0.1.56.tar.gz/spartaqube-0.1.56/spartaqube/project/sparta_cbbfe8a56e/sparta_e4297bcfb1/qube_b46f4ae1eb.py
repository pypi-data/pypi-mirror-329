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
from project.sparta_662ef67a08.sparta_de50df2b96 import qube_402b72174d as qube_402b72174d
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_0d16fbb533
@csrf_exempt
@sparta_0d16fbb533
def sparta_6b39d6ebb6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_402b72174d.sparta_6b39d6ebb6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_c9a28b9313(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_402b72174d.sparta_c9a28b9313(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_0d16fbb533
def sparta_dd75215bf0(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_402b72174d.sparta_dd75215bf0(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_0d16fbb533
def sparta_efd9853b6a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_402b72174d.sparta_efd9853b6a(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_c3f27b72b4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_402b72174d.sparta_c3f27b72b4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_0d16fbb533
def sparta_3064333930(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_402b72174d.sparta_3064333930(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_22bb3d9803(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_402b72174d.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_0d16fbb533
def sparta_c26ee0e6b7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_402b72174d.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_4620109a44(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_402b72174d.sparta_4620109a44(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_603fd2b697(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_402b72174d.sparta_603fd2b697(A,C);E=json.dumps(D);return HttpResponse(E)