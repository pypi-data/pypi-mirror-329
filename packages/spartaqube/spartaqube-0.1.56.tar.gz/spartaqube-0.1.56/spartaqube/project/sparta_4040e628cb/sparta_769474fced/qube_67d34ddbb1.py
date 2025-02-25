import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
import project.sparta_3500f2f8a8.sparta_c6eb62a0d0.qube_0ad4e25f38 as qube_0ad4e25f38
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_f93fd87579
from project.sparta_662ef67a08.sparta_928c4c5c7e import qube_8088811bba as qube_8088811bba
from project.sparta_662ef67a08.sparta_9caf5c932d import qube_8d35301237 as qube_8d35301237
def sparta_a93cc5ef0f():
	A=platform.system()
	if A=='Windows':return'windows'
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_f93fd87579
@login_required(redirect_field_name='login')
def sparta_eebe9492b3(request):
	E='template';D='developer';B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_0ad4e25f38.sparta_1ab7a89a58(B);return render(B,'dist/project/homepage/homepage.html',A)
	A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A['menuBar']=12;F=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(F);A['bCodeMirror']=True;G=os.path.dirname(__file__);C=os.path.dirname(os.path.dirname(G));H=os.path.join(C,'static');I=os.path.join(H,'js',D,E,'frontend');A['frontend_path']=I;J=os.path.dirname(C);K=os.path.join(J,'django_app_template',D,E,'backend');A['backend_path']=K;return render(B,'dist/project/developer/developerExamples.html',A)