from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings as conf_settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import hashlib,project.sparta_8da3d59761.sparta_e1d65002c1.qube_87c1dfb7e8 as qube_87c1dfb7e8
from project.sparta_0c8b5020ad.sparta_c704a8bec8.qube_8bc7be3e5f import sparta_b83c31242b
@csrf_exempt
def sparta_038907d889(request):B=request;A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);A['menuBar']=8;A['bCodeMirror']=True;C=qube_87c1dfb7e8.sparta_cb8781f955(B.user);A.update(C);return render(B,'dist/project/api/api.html',A)