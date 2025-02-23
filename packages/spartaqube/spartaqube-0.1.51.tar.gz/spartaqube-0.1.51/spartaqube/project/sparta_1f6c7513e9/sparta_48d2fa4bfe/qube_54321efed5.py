import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
import project.sparta_3c031cc253.sparta_8fd6b56ef0.qube_d80062ebbf as qube_d80062ebbf
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff.qube_0e0a02b9a2 import sparta_5b0a6b77e6
from project.sparta_ab7a1c0e2d.sparta_6016211a05 import qube_98ebf6e674 as qube_98ebf6e674
from project.sparta_ab7a1c0e2d.sparta_3d65dcb7bc import qube_3092ed132a as qube_3092ed132a
def sparta_40fbb95963():
	A=platform.system()
	if A=='Windows':return'windows'
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_5b0a6b77e6
@login_required(redirect_field_name='login')
def sparta_a8ae62fdff(request):
	E='template';D='developer';B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_d80062ebbf.sparta_5554065f87(B);return render(B,'dist/project/homepage/homepage.html',A)
	A=qube_d80062ebbf.sparta_5554065f87(B);A['menuBar']=12;F=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(F);A['bCodeMirror']=True;G=os.path.dirname(__file__);C=os.path.dirname(os.path.dirname(G));H=os.path.join(C,'static');I=os.path.join(H,'js',D,E,'frontend');A['frontend_path']=I;J=os.path.dirname(C);K=os.path.join(J,'django_app_template',D,E,'backend');A['backend_path']=K;return render(B,'dist/project/developer/developerExamples.html',A)