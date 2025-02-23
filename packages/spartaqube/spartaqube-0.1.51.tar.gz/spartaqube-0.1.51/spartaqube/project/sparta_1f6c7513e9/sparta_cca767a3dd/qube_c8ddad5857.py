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
import project.sparta_3c031cc253.sparta_8fd6b56ef0.qube_d80062ebbf as qube_d80062ebbf
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff.qube_0e0a02b9a2 import sparta_5b0a6b77e6
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff import qube_0e0a02b9a2 as qube_0e0a02b9a2
from project.sparta_b3c5acfd41.sparta_e5e98a49fb import qube_0556612538 as qube_0556612538
from project.models import LoginLocation,UserProfile
def sparta_30af4021c4():return{'bHasCompanyEE':-1}
def sparta_a658c3b293(request):B=request;A=qube_d80062ebbf.sparta_5554065f87(B);A[_C]=qube_d80062ebbf.sparta_bfdefaa8a9();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_5b0a6b77e6
def sparta_0046de2fa1(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_8bf66c241b(C,A)
def sparta_592b04f1f0(request,redirectUrl):return sparta_8bf66c241b(request,redirectUrl)
def sparta_8bf66c241b(request,redirectUrl):
	E=redirectUrl;A=request;print('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_0e0a02b9a2.sparta_d217d06e15(F):return sparta_a658c3b293(A)
				login(A,F);K,L=qube_d80062ebbf.sparta_3afd25f68d();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_d80062ebbf.sparta_5554065f87(A);B.update(qube_d80062ebbf.sparta_1739123101(A));B[_C]=qube_d80062ebbf.sparta_bfdefaa8a9();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_30af4021c4());return render(A,'dist/project/auth/login.html',B)
def sparta_2ceb156efa(request):
	B='public@spartaqube.com';A=User.objects.filter(email=B).all()
	if A.count()>0:C=A[0];login(request,C)
	return redirect(_D)
@sparta_5b0a6b77e6
def sparta_35fe42fb95(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_0e0a02b9a2.sparta_dc3d300bc8()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_0e0a02b9a2.sparta_413fe415e5(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_0e0a02b9a2.sparta_0606a7cae6(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_d80062ebbf.sparta_5554065f87(A);C.update(qube_d80062ebbf.sparta_1739123101(A));C[_C]=qube_d80062ebbf.sparta_bfdefaa8a9();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_30af4021c4());return render(A,'dist/project/auth/registration.html',C)
def sparta_1558363199(request):A=request;B=qube_d80062ebbf.sparta_5554065f87(A);B[_C]=qube_d80062ebbf.sparta_bfdefaa8a9();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_580d4c7c03(request,token):
	A=request;B=qube_0e0a02b9a2.sparta_c491b7da32(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_d80062ebbf.sparta_5554065f87(A);D[_C]=qube_d80062ebbf.sparta_bfdefaa8a9();return redirect(_I)
def sparta_d578df4317(request):logout(request);return redirect(_I)
def sparta_77fdb585ed(request):
	A=request
	if A.user.is_authenticated:
		if A.user.email=='cypress_tests@gmail.com':A.user.delete()
	logout(A);return redirect(_I)
def sparta_a0fb8e64af(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_371c27ebe8(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_0e0a02b9a2.sparta_371c27ebe8(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_d80062ebbf.sparta_5554065f87(A);C.update(qube_d80062ebbf.sparta_1739123101(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_d80062ebbf.sparta_bfdefaa8a9();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:print('exception ');print(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_d80062ebbf.sparta_5554065f87(A);D.update(qube_d80062ebbf.sparta_1739123101(A));D[_C]=qube_d80062ebbf.sparta_bfdefaa8a9();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_30af4021c4());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_73c653feb3(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_0e0a02b9a2.sparta_73c653feb3(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_d80062ebbf.sparta_5554065f87(D);A.update(qube_d80062ebbf.sparta_1739123101(D));A[_C]=qube_d80062ebbf.sparta_bfdefaa8a9();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_30af4021c4());return render(D,_N,A)