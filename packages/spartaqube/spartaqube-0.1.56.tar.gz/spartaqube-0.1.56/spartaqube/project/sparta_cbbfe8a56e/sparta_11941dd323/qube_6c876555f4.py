_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_662ef67a08.sparta_997924947f import qube_49801d5f14 as qube_49801d5f14
from project.sparta_662ef67a08.sparta_c82afc7e55 import qube_fd92bf22a4 as qube_fd92bf22a4
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_0d16fbb533
@csrf_exempt
@sparta_0d16fbb533
def sparta_ac684225a5(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_fd92bf22a4.sparta_f8f41432ed(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_49801d5f14.sparta_ac684225a5(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_0d16fbb533
def sparta_cb2b43dbc8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_49801d5f14.sparta_e985f2a713(C,A.user);E=json.dumps(D);return HttpResponse(E)