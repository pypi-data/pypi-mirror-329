from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings as conf_settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import hashlib,project.sparta_3c031cc253.sparta_8fd6b56ef0.qube_d80062ebbf as qube_d80062ebbf
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff.qube_0e0a02b9a2 import sparta_5b0a6b77e6
@csrf_exempt
def sparta_e01126ca43(request):B=request;A=qube_d80062ebbf.sparta_5554065f87(B);A['menuBar']=8;A['bCodeMirror']=True;C=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(C);return render(B,'dist/project/api/api.html',A)