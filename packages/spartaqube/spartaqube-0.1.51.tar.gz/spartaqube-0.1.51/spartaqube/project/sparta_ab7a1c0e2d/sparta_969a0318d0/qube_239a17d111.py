import re,os,json,requests
from datetime import datetime
from packaging.version import parse
from project.models import AppVersioning
import pytz
UTC=pytz.utc
def sparta_cf463444e0():0
def sparta_74081d2a5a():A='name';B='https://api.github.com/repos/SpartaQube/spartaqube-version/tags';C=requests.get(B);D=json.loads(C.text);E=max(D,key=lambda t:parse(t[A]));return E[A]
def sparta_9fdd6cc27b():A='https://spartaqube-version.pages.dev/latest_version.txt';B=requests.get(A);return B.text.split('\n')[0]
def sparta_14ef24c78d():
	try:A='https://pypi.org/project/spartaqube/';B=requests.get(A).text;C=re.search('<h1 class="package-header__name">(.*?)</h1>',B,re.DOTALL);D=C.group(1);E=D.strip().split('spartaqube ')[1];return E
	except:pass
def sparta_e9605efc3e():
	B=os.path.dirname(__file__);C=os.path.dirname(B);D=os.path.dirname(C);E=os.path.dirname(D)
	try:
		with open(os.path.join(E,'app_version.json'),'r')as F:G=json.load(F);A=G['version']
	except:A='0.1.1'
	return A
def sparta_5a8f32178f():
	G='res'
	try:
		B=sparta_e9605efc3e();A=sparta_9fdd6cc27b();print(f"current_version: {B} and latest_version {A}");D=AppVersioning.objects.all();E=datetime.now().astimezone(UTC)
		if D.count()==0:AppVersioning.objects.create(last_available_version_pip=A,last_check_date=E)
		else:C=D[0];C.last_available_version_pip=A;C.last_check_date=E;C.save()
		return{'current_version':B,'latest_version':A,'b_update':not B==A,'humanDate':'A moment ago',G:1}
	except Exception as F:print('Exception versioning update');print(F);return{G:-1,'errorMsg':str(F)}