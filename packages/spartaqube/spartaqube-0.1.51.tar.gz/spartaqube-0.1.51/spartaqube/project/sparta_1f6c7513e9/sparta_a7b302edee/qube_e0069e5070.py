from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_3c031cc253.sparta_8fd6b56ef0.qube_d80062ebbf as qube_d80062ebbf
from project.models import UserProfile
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff.qube_0e0a02b9a2 import sparta_5b0a6b77e6
from project.sparta_1f6c7513e9.sparta_cca767a3dd.qube_c8ddad5857 import sparta_30af4021c4
@sparta_5b0a6b77e6
@login_required(redirect_field_name='login')
def sparta_50976caa28(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_d80062ebbf.sparta_5554065f87(B);A.update(qube_d80062ebbf.sparta_0f86a5807b(B.user));A.update(F);G='';A['accessKey']=G;A['menuBar']=4;A.update(sparta_30af4021c4());return render(B,'dist/project/auth/settings.html',A)