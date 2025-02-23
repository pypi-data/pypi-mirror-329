_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_ab7a1c0e2d.sparta_e50c345294 import qube_974654c621 as qube_974654c621
from project.sparta_ab7a1c0e2d.sparta_3670d291b3 import qube_d8efa5f6c9 as qube_d8efa5f6c9
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff.qube_0e0a02b9a2 import sparta_22afa6a0c1
@csrf_exempt
@sparta_22afa6a0c1
def sparta_d78ebb91bb(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_d8efa5f6c9.sparta_6841f17a84(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_974654c621.sparta_d78ebb91bb(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_22afa6a0c1
def sparta_d5b20bcc4a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_974654c621.sparta_11a0ae56c9(C,A.user);E=json.dumps(D);return HttpResponse(E)