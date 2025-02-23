from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_ab7a1c0e2d.sparta_d43bee19ff.qube_0e0a02b9a2 import sparta_5b0a6b77e6
from project.sparta_ab7a1c0e2d.sparta_3670d291b3 import qube_d8efa5f6c9 as qube_d8efa5f6c9
from project.models import UserProfile
import project.sparta_3c031cc253.sparta_8fd6b56ef0.qube_d80062ebbf as qube_d80062ebbf
@sparta_5b0a6b77e6
@login_required(redirect_field_name='login')
def sparta_d46d4ca3cd(request):
	E='avatarImg';B=request;A=qube_d80062ebbf.sparta_5554065f87(B);A['menuBar']=-1;F=qube_d80062ebbf.sparta_0f86a5807b(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_5b0a6b77e6
@login_required(redirect_field_name='login')
def sparta_9093516b5c(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_d46d4ca3cd(A)