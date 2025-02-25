import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_662ef67a08.sparta_c7046022a7 import qube_9d9c7918e0 as qube_9d9c7918e0
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_0d16fbb533
@csrf_exempt
@sparta_0d16fbb533
def sparta_fbd4a8db48(request):G='api_func';F='key';E='utf-8';A=request;C=A.body.decode(E);C=A.POST.get(F);D=A.body.decode(E);D=A.POST.get(G);B=dict();B[F]=C;B[G]=D;H=qube_9d9c7918e0.sparta_fbd4a8db48(B,A.user);I=json.dumps(H);return HttpResponse(I)