from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_8da3d59761.sparta_e1d65002c1.qube_87c1dfb7e8 as qube_87c1dfb7e8
from project.models import UserProfile
from project.sparta_0c8b5020ad.sparta_c704a8bec8.qube_8bc7be3e5f import sparta_b83c31242b
from project.sparta_1f3dab4412.sparta_a8c4e00965.qube_642dc57ef9 import sparta_fefd5b3e39
@sparta_b83c31242b
@login_required(redirect_field_name='login')
def sparta_85f8e6dcfb(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);A.update(qube_87c1dfb7e8.sparta_cb8781f955(B.user));A.update(F);G='';A['accessKey']=G;A['menuBar']=4;A.update(sparta_fefd5b3e39());return render(B,'dist/project/auth/settings.html',A)