from datetime import datetime
import hashlib,os,sys,django
def sparta_4451809d4d():C='/';B='\\';D=os.path.dirname(os.path.abspath(__file__)).replace(B,C);A=os.path.dirname(D).replace(B,C);A=os.path.dirname(A).replace(B,C);A=os.path.dirname(A).replace(B,C);sys.path.append(A);print('oneLevelUpPath');print(A);os.environ.setdefault('DJANGO_SETTINGS_MODULE','spartaqube_app.settings');os.environ['DJANGO_ALLOW_ASYNC_UNSAFE']='true';django.setup()
def sparta_05d93e87e3():
	H='utf-8';B='admin';from django.contrib.auth.models import User as G;from project.models import UserProfile as I
	if not G.objects.filter(username=B).exists():C='admin@spartaqube.com';A=G.objects.create_user(B,first_name=B,last_name=B,email=C,password=B);A.is_superuser=True;A.is_staff=True;A.save();D=I(user=A);E=str(A.id)+'_'+str(A.email);E=E.encode(H);F=hashlib.md5(E).hexdigest()+str(datetime.now());F=F.encode(H);D.userId=hashlib.sha256(F).hexdigest();D.email=C;D.save();print(f"Admin {C} created")
if __name__=='__main__':sparta_4451809d4d();sparta_05d93e87e3()