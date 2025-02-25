import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_0d16fbb533
from project.sparta_662ef67a08.sparta_b79472fa7e import qube_0e2abbf88a as qube_0e2abbf88a
@csrf_exempt
@sparta_0d16fbb533
def sparta_bc4c406c10(request):A=request;B=json.loads(A.body);C=json.loads(B['jsonData']);D=A.user;E=qube_0e2abbf88a.sparta_bc4c406c10(C,D);F=json.dumps(E);return HttpResponse(F)