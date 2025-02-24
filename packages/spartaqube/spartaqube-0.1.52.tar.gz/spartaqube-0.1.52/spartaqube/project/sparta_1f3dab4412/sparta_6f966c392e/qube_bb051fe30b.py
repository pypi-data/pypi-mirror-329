import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
import project.sparta_8da3d59761.sparta_e1d65002c1.qube_87c1dfb7e8 as qube_87c1dfb7e8
from project.sparta_0c8b5020ad.sparta_c704a8bec8.qube_8bc7be3e5f import sparta_b83c31242b
from project.sparta_0c8b5020ad.sparta_bf728a6b22 import qube_7f065f2f14 as qube_7f065f2f14
from project.sparta_0c8b5020ad.sparta_1aad359281 import qube_febb5b69bd as qube_febb5b69bd
def sparta_7e22b2c145():
	A=platform.system()
	if A=='Windows':return'windows'
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_b83c31242b
@login_required(redirect_field_name='login')
def sparta_413576a984(request):
	E='template';D='developer';B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);return render(B,'dist/project/homepage/homepage.html',A)
	A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);A['menuBar']=12;F=qube_87c1dfb7e8.sparta_cb8781f955(B.user);A.update(F);A['bCodeMirror']=True;G=os.path.dirname(__file__);C=os.path.dirname(os.path.dirname(G));H=os.path.join(C,'static');I=os.path.join(H,'js',D,E,'frontend');A['frontend_path']=I;J=os.path.dirname(C);K=os.path.join(J,'django_app_template',D,E,'backend');A['backend_path']=K;return render(B,'dist/project/developer/developerExamples.html',A)