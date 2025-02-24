_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_0c8b5020ad.sparta_8611b07055 import qube_8ad80460d6 as qube_8ad80460d6
from project.sparta_0c8b5020ad.sparta_92e12ff929 import qube_ea308ffebe as qube_ea308ffebe
from project.sparta_0c8b5020ad.sparta_c704a8bec8.qube_8bc7be3e5f import sparta_3e75bbbf32
@csrf_exempt
@sparta_3e75bbbf32
def sparta_a8da42e637(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_ea308ffebe.sparta_a123e76702(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_8ad80460d6.sparta_a8da42e637(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_3e75bbbf32
def sparta_fca7ab0f83(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_8ad80460d6.sparta_d0efed9f55(C,A.user);E=json.dumps(D);return HttpResponse(E)