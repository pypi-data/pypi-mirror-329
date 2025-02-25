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
import project.sparta_3500f2f8a8.sparta_c6eb62a0d0.qube_0ad4e25f38 as qube_0ad4e25f38
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_f93fd87579
from project.sparta_662ef67a08.sparta_1616d6b2d2 import qube_381eed7f1c as qube_381eed7f1c
from project.sparta_cbbfe8a56e.sparta_576072c67c import qube_b69afc6108 as qube_b69afc6108
from project.models import LoginLocation,UserProfile
from project.logger_config import logger
def sparta_aae7531102():return{'bHasCompanyEE':-1}
def sparta_afd07618cd(request):B=request;A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A[_C]=qube_0ad4e25f38.sparta_74457c1c00();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_f93fd87579
def sparta_0054bc5464(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_580d1d21f4(C,A)
def sparta_211ae35e0a(request,redirectUrl):return sparta_580d1d21f4(request,redirectUrl)
def sparta_580d1d21f4(request,redirectUrl):
	E=redirectUrl;A=request;logger.debug('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_381eed7f1c.sparta_6a7505270d(F):return sparta_afd07618cd(A)
				login(A,F);K,L=qube_0ad4e25f38.sparta_6ac3fc76f3();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_0ad4e25f38.sparta_1ab7a89a58(A);B.update(qube_0ad4e25f38.sparta_c791aea08f(A));B[_C]=qube_0ad4e25f38.sparta_74457c1c00();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_aae7531102());return render(A,'dist/project/auth/login.html',B)
def sparta_7f45cb16e8(request):
	B='public@spartaqube.com';A=User.objects.filter(email=B).all()
	if A.count()>0:C=A[0];login(request,C)
	return redirect(_D)
@sparta_f93fd87579
def sparta_b9399c7eb4(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_381eed7f1c.sparta_fcfd197ed9()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_381eed7f1c.sparta_5eeff52cf7(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_381eed7f1c.sparta_27448efe57(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_0ad4e25f38.sparta_1ab7a89a58(A);C.update(qube_0ad4e25f38.sparta_c791aea08f(A));C[_C]=qube_0ad4e25f38.sparta_74457c1c00();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_aae7531102());return render(A,'dist/project/auth/registration.html',C)
def sparta_f705714048(request):A=request;B=qube_0ad4e25f38.sparta_1ab7a89a58(A);B[_C]=qube_0ad4e25f38.sparta_74457c1c00();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_1555849ab6(request,token):
	A=request;B=qube_381eed7f1c.sparta_433d0455a0(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_0ad4e25f38.sparta_1ab7a89a58(A);D[_C]=qube_0ad4e25f38.sparta_74457c1c00();return redirect(_I)
def sparta_ad8949db43(request):logout(request);return redirect(_I)
def sparta_043fb46e8b(request):
	A=request
	if A.user.is_authenticated:
		if A.user.email=='cypress_tests@gmail.com':A.user.delete()
	logout(A);return redirect(_I)
def sparta_ba100cf890(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_89b110d83a(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_381eed7f1c.sparta_89b110d83a(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_0ad4e25f38.sparta_1ab7a89a58(A);C.update(qube_0ad4e25f38.sparta_c791aea08f(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_0ad4e25f38.sparta_74457c1c00();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:logger.debug('exception ');logger.debug(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_0ad4e25f38.sparta_1ab7a89a58(A);D.update(qube_0ad4e25f38.sparta_c791aea08f(A));D[_C]=qube_0ad4e25f38.sparta_74457c1c00();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_aae7531102());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_46e1acaa0f(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_381eed7f1c.sparta_46e1acaa0f(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_0ad4e25f38.sparta_1ab7a89a58(D);A.update(qube_0ad4e25f38.sparta_c791aea08f(D));A[_C]=qube_0ad4e25f38.sparta_74457c1c00();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_aae7531102());return render(D,_N,A)