_A='backend'
import os,sys,json,importlib,traceback,asyncio,subprocess,platform
from django.conf import settings
from pathlib import Path
from channels.generic.websocket import WebsocketConsumer
from spartaqube_app.path_mapper_obf import sparta_eb692a7fc2
from project.sparta_662ef67a08.sparta_bc02ea2c9b.qube_2ac5797abc import sparta_6fbba8ac09
from project.sparta_662ef67a08.sparta_c60717777a.qube_76e4aadc41 import IPythonKernel as IPythonKernel
from project.sparta_662ef67a08.sparta_054f72bfca.qube_e384b55d37 import SenderKernel
from project.sparta_662ef67a08.sparta_dbb6ae3cca.qube_38ccf7dba7 import sparta_a70ad7bec7,sparta_7245720e20
from project.logger_config import logger
class OutputRedirector:
	def __init__(A,websocket):A.websocket=websocket;A.original_stdout=sys.stdout;A.original_stderr=sys.stderr
	def __enter__(A):
		class B:
			def __init__(A,websocket):A.websocket=websocket
			def write(A,message):
				if A.websocket:
					try:A.websocket.send(json.dumps({'res':1000,'msg':message}))
					except Exception as B:logger.debug(f"WebSocket send error: {B}")
		A.custom_stream=B(A.websocket);sys.stdout=A.custom_stream;sys.stderr=A.custom_stream
	def __exit__(A,exc_type,exc_val,exc_tb):sys.stdout=A.original_stdout;sys.stderr=A.original_stderr
class ApiWebserviceWS(WebsocketConsumer):
	def create_kernel_in_global_kernel_manager(A,kernel_manager_uuid):from project.sparta_662ef67a08.sparta_054f72bfca import qube_c08e7e260b as B;C=2;D='';E=A.user;F=B.SqKernelManager(kernel_manager_uuid,C,D,E);F.create_kernel()
	def sparta_85a80decb3(B,kernel_manager_uuid):
		A=kernel_manager_uuid
		if A not in settings.GLOBAL_KERNEL_MANAGER:B.create_kernel_in_global_kernel_manager(A)
		return settings.GLOBAL_KERNEL_MANAGER[A].ipython_kernel
	def is_init_kernel(B,kernel_manager_uuid):
		A=kernel_manager_uuid
		if A not in settings.GLOBAL_KERNEL_MANAGER:B.create_kernel_in_global_kernel_manager(A)
		return settings.GLOBAL_KERNEL_MANAGER[A].is_init
	def connect(A):logger.debug('Connect Now');A.user=A.scope['user'];A.accept()
	def disconnect(A,close_code=None):logger.debug('Disconnect')
	async def create_kernel(A):B=sparta_7245720e20(A.user);return await IPythonKernel(api_key=B,django_settings_module='app.settings')
	def init_kernel_import_models(A,kernel_manager_uuid,user_project_path):
		B=kernel_manager_uuid
		if not A.is_init_kernel(B):D=os.path.join(os.path.dirname(user_project_path),_A);C=os.path.join(D,'app');E=f'''
%load_ext autoreload
%autoreload 2    
import os, sys
import django
# Set the Django settings module
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
sys.path.insert(0, r"{C}")
os.chdir(r"{C}")
os.environ[\'DJANGO_SETTINGS_MODULE\'] = \'app.settings\'
# Initialize Django
django.setup()
''';A.get_ipython_kernel_obj(B).execute_code(E,websocket=A);settings.GLOBAL_KERNEL_MANAGER[B].is_init=True
	def receive(A,text_data):
		F=text_data
		if len(F)>0:
			C=json.loads(F);D=C['kernelManagerUUID'];K=C.get('isRunMode',False);G=sparta_6fbba8ac09(C['baseProjectPath']);H=os.path.join(os.path.dirname(G),_A);I=C['service'];J=C.copy();A.init_kernel_import_models(D,G);B='import os, sys, importlib\n';B+=f'sys.path.insert(0, r"{H}")\n';B+=f"import webservices\n";B+=f"importlib.reload(webservices)\n";B+=f"webservice_res_dict = webservices.sparta_89e9f27ee5(service_name, post_data)\n";logger.debug('code_to_exec');logger.debug(B);A.get_ipython_kernel_obj(D).set_workspace_variables({'service_name':I,'post_data':J});A.get_ipython_kernel_obj(D).execute_code(B,websocket=A);E=A.get_ipython_kernel_obj(D).get_workspace_variable('webservice_res_dict')
			if E is not None:E['webservice_resolve']=1;A.send(json.dumps(E))