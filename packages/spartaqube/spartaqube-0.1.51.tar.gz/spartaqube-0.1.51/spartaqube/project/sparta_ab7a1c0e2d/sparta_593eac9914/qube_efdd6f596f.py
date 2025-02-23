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
from project.sparta_ab7a1c0e2d.sparta_9130611051 import qube_fb51653a52 as qube_fb51653a52
def sparta_bac2585bca(is_owner=_A):return{_F:is_owner,_B:_E,_C:_E,_D:_E}
def sparta_613b557a27():return{_F:_A,_B:_A,_C:_A,_D:_A}
def sparta_95d92922d8(user_obj,portfolio_obj):
	B=portfolio_obj;A=user_obj
	if B.user==A:return sparta_bac2585bca(_E)
	F=qube_fb51653a52.sparta_cf779a69b7(A);E=[A.userGroup for A in F]
	if len(E)>0:D=PortfolioShared.objects.filter(Q(is_delete=0,userGroup__in=E,portfolio=B)&~Q(portfolio__user=A)|Q(is_delete=0,user=A,portfolio=B))
	else:D=PortfolioShared.objects.filter(is_delete=0,user=A,portfolio=B)
	if D.count()==0:return sparta_613b557a27()
	G=D[0];C=G.ShareRights
	if C.is_delete:return sparta_613b557a27()
	return{_F:_A,_B:C.is_admin,_C:C.has_write_rights,_D:C.has_reshare_rights}
def sparta_d71cde8244(user_obj,universe_obj):
	B=universe_obj;A=user_obj
	if B.user==A:return sparta_bac2585bca()
	F=qube_fb51653a52.sparta_cf779a69b7(A);E=[A.userGroup for A in F]
	if len(E)>0:D=UniverseShared.objects.filter(Q(is_delete=0,userGroup__in=E,universe=B)&~Q(universe__user=A)|Q(is_delete=0,user=A,universe=B))
	else:D=UniverseShared.objects.filter(is_delete=0,user=A,universe=B)
	if D.count()==0:return sparta_613b557a27()
	G=D[0];C=G.ShareRights
	if C.is_delete:return sparta_613b557a27()
	return{_B:C.is_admin,_C:C.has_write_rights,_D:C.has_reshare_rights}