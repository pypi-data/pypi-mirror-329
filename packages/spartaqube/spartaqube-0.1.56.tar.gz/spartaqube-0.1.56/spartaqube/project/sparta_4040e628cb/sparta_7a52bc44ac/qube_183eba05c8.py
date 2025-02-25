from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_662ef67a08.sparta_1616d6b2d2.qube_381eed7f1c import sparta_f93fd87579
from project.sparta_662ef67a08.sparta_c82afc7e55 import qube_fd92bf22a4 as qube_fd92bf22a4
from project.models import UserProfile
import project.sparta_3500f2f8a8.sparta_c6eb62a0d0.qube_0ad4e25f38 as qube_0ad4e25f38
@sparta_f93fd87579
@login_required(redirect_field_name='login')
def sparta_9089564407(request):
	E='avatarImg';B=request;A=qube_0ad4e25f38.sparta_1ab7a89a58(B);A['menuBar']=-1;F=qube_0ad4e25f38.sparta_e08ad78749(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_f93fd87579
@login_required(redirect_field_name='login')
def sparta_6029c35ae9(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_9089564407(A)