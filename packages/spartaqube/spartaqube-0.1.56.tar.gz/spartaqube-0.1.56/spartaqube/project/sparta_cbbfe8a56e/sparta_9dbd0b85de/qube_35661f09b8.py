import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_662ef67a08.sparta_3b64fa15ab import qube_0c1beab159 as qube_0c1beab159
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_0d16fbb533,sparta_2c86a953f4
@csrf_exempt
@sparta_0d16fbb533
def sparta_eda8220846(request):A=request;B=json.loads(A.body);C=json.loads(B['jsonData']);D=qube_0c1beab159.sparta_eda8220846(C,A.user);E=json.dumps(D);return HttpResponse(E)