from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_0c8b5020ad.sparta_c704a8bec8.qube_8bc7be3e5f import sparta_b83c31242b
from project.sparta_0c8b5020ad.sparta_92e12ff929 import qube_ea308ffebe as qube_ea308ffebe
from project.models import UserProfile
import project.sparta_8da3d59761.sparta_e1d65002c1.qube_87c1dfb7e8 as qube_87c1dfb7e8
@sparta_b83c31242b
@login_required(redirect_field_name='login')
def sparta_c08905d3a4(request):
	E='avatarImg';B=request;A=qube_87c1dfb7e8.sparta_2dd044b9fe(B);A['menuBar']=-1;F=qube_87c1dfb7e8.sparta_cb8781f955(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_b83c31242b
@login_required(redirect_field_name='login')
def sparta_670257a4bb(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_c08905d3a4(A)