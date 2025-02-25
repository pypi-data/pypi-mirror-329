from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_3500f2f8a8.sparta_c6eb62a0d0.qube_0ad4e25f38 as qube_0ad4e25f38
from project.models import UserProfile
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_f93fd87579
from project.sparta_4040e628cb.sparta_031d1cf027.qube_42fde51afd import sparta_aae7531102
@sparta_f93fd87579
@login_required(redirect_field_name='login')
def sparta_98ae9f1ca3(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A.update(qube_0ad4e25f38.sparta_e08ad78749(B.user));A.update(F);G='';A['accessKey']=G;A['menuBar']=4;A.update(sparta_aae7531102());return render(B,'dist/project/auth/settings.html',A)