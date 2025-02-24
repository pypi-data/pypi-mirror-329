_O='Please send valid data'
_N='dist/project/auth/resetPasswordChange.html'
_M='captcha'
_L='password'
_K='POST'
_J=False
_I='login'
_H='error'
_G='form'
_F='email'
_E='res'
_D='home'
_C='manifest'
_B='errorMsg'
_A=True
import json,hashlib,uuid
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.urls import reverse
import project.sparta_8da3d59761.sparta_e1d65002c1.qube_87c1dfb7e8 as qube_87c1dfb7e8
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_0c8b5020ad.sparta_c704a8bec8.qube_8bc7be3e5f import sparta_b83c31242b
from project.sparta_0c8b5020ad.sparta_c704a8bec8 import qube_8bc7be3e5f as qube_8bc7be3e5f
from project.sparta_a986990c47.sparta_7a5dfd51b4 import qube_c8783b6a95 as qube_c8783b6a95
from project.models import LoginLocation,UserProfile
from project.logger_config import logger
def sparta_fefd5b3e39():return{'bHasCompanyEE':-1}
def sparta_aa9f26ea3b(request):B=request;A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);A[_C]=qube_87c1dfb7e8.sparta_6c5c3f30a2();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_b83c31242b
def sparta_2e47e6b1cd(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_2404a32b7e(C,A)
def sparta_08119e304e(request,redirectUrl):return sparta_2404a32b7e(request,redirectUrl)
def sparta_2404a32b7e(request,redirectUrl):
	E=redirectUrl;A=request;logger.debug('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_8bc7be3e5f.sparta_9390a85fac(F):return sparta_aa9f26ea3b(A)
				login(A,F);K,L=qube_87c1dfb7e8.sparta_0668722074();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_87c1dfb7e8.sparta_2dd044b9fe(A);B.update(qube_87c1dfb7e8.sparta_47bc78d099(A));B[_C]=qube_87c1dfb7e8.sparta_6c5c3f30a2();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_fefd5b3e39());return render(A,'dist/project/auth/login.html',B)
def sparta_b27f8f098e(request):
	B='public@spartaqube.com';A=User.objects.filter(email=B).all()
	if A.count()>0:C=A[0];login(request,C)
	return redirect(_D)
@sparta_b83c31242b
def sparta_518d601a43(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_8bc7be3e5f.sparta_66ea5204ff()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_8bc7be3e5f.sparta_31b292360d(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_8bc7be3e5f.sparta_55966fc13d(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_87c1dfb7e8.sparta_2dd044b9fe(A);C.update(qube_87c1dfb7e8.sparta_47bc78d099(A));C[_C]=qube_87c1dfb7e8.sparta_6c5c3f30a2();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_fefd5b3e39());return render(A,'dist/project/auth/registration.html',C)
def sparta_8b8857788c(request):A=request;B=qube_87c1dfb7e8.sparta_2dd044b9fe(A);B[_C]=qube_87c1dfb7e8.sparta_6c5c3f30a2();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_2b87188a97(request,token):
	A=request;B=qube_8bc7be3e5f.sparta_bb84e0cd1f(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_87c1dfb7e8.sparta_2dd044b9fe(A);D[_C]=qube_87c1dfb7e8.sparta_6c5c3f30a2();return redirect(_I)
def sparta_34a698d9fa(request):logout(request);return redirect(_I)
def sparta_9bc9bfee4f(request):
	A=request
	if A.user.is_authenticated:
		if A.user.email=='cypress_tests@gmail.com':A.user.delete()
	logout(A);return redirect(_I)
def sparta_3089de52c1(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_9698b56edb(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_8bc7be3e5f.sparta_9698b56edb(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_87c1dfb7e8.sparta_2dd044b9fe(A);C.update(qube_87c1dfb7e8.sparta_47bc78d099(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_87c1dfb7e8.sparta_6c5c3f30a2();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:logger.debug('exception ');logger.debug(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_87c1dfb7e8.sparta_2dd044b9fe(A);D.update(qube_87c1dfb7e8.sparta_47bc78d099(A));D[_C]=qube_87c1dfb7e8.sparta_6c5c3f30a2();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_fefd5b3e39());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_41fb4e15e4(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_8bc7be3e5f.sparta_41fb4e15e4(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_87c1dfb7e8.sparta_2dd044b9fe(D);A.update(qube_87c1dfb7e8.sparta_47bc78d099(D));A[_C]=qube_87c1dfb7e8.sparta_6c5c3f30a2();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_fefd5b3e39());return render(D,_N,A)