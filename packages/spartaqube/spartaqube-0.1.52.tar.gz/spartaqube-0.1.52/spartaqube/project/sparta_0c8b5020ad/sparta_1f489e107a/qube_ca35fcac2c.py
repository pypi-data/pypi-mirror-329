_F='is_owner'
_E=True
_D='has_reshare_rights'
_C='has_write_rights'
_B='is_admin'
_A=False
import json,base64,hashlib,re,uuid,pandas as pd
from datetime import datetime,timedelta
from dateutil import parser
import pytz
UTC=pytz.utc
from django.db.models import Q
from django.conf import settings as conf_settings
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturalday
from django.forms.models import model_to_dict
from project.models import User,UserProfile
from project.sparta_0c8b5020ad.sparta_da6af08d87 import qube_c77b125770 as qube_c77b125770
def sparta_2c195efa30(is_owner=_A):return{_F:is_owner,_B:_E,_C:_E,_D:_E}
def sparta_173ff549bb():return{_F:_A,_B:_A,_C:_A,_D:_A}
def sparta_389694e85c(user_obj,portfolio_obj):
	B=portfolio_obj;A=user_obj
	if B.user==A:return sparta_2c195efa30(_E)
	F=qube_c77b125770.sparta_75b909e585(A);E=[A.userGroup for A in F]
	if len(E)>0:D=PortfolioShared.objects.filter(Q(is_delete=0,userGroup__in=E,portfolio=B)&~Q(portfolio__user=A)|Q(is_delete=0,user=A,portfolio=B))
	else:D=PortfolioShared.objects.filter(is_delete=0,user=A,portfolio=B)
	if D.count()==0:return sparta_173ff549bb()
	G=D[0];C=G.ShareRights
	if C.is_delete:return sparta_173ff549bb()
	return{_F:_A,_B:C.is_admin,_C:C.has_write_rights,_D:C.has_reshare_rights}
def sparta_1eff406985(user_obj,universe_obj):
	B=universe_obj;A=user_obj
	if B.user==A:return sparta_2c195efa30()
	F=qube_c77b125770.sparta_75b909e585(A);E=[A.userGroup for A in F]
	if len(E)>0:D=UniverseShared.objects.filter(Q(is_delete=0,userGroup__in=E,universe=B)&~Q(universe__user=A)|Q(is_delete=0,user=A,universe=B))
	else:D=UniverseShared.objects.filter(is_delete=0,user=A,universe=B)
	if D.count()==0:return sparta_173ff549bb()
	G=D[0];C=G.ShareRights
	if C.is_delete:return sparta_173ff549bb()
	return{_B:C.is_admin,_C:C.has_write_rights,_D:C.has_reshare_rights}