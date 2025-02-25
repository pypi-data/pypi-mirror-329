_O='stdout'
_N='windows'
_M='idle'
_L='busy'
_K='exec'
_J='service'
_I='type'
_H='data'
_G='res'
_F='name'
_E=False
_D='execution_state'
_C='output'
_B='content'
_A=None
import os,gc,re,json,time,websocket,cloudpickle,base64,getpass,platform,asyncio
from pathlib import Path
from jupyter_client import KernelManager
from IPython.display import display,Javascript
from IPython.core.magics.namespace import NamespaceMagics
from nbconvert.filters import strip_ansi
from django.conf import settings as conf_settings
from project.sparta_3500f2f8a8.qube_682114d599 import timeout
from project.sparta_662ef67a08.sparta_bc02ea2c9b.qube_2ac5797abc import convert_to_dataframe,sparta_6fbba8ac09
from project.logger_config import logger
B_DEBUG=_E
SEND_INTERVAL=.5
def sparta_40d9acc6f9():return conf_settings.DEFAULT_TIMEOUT
def sparta_a93cc5ef0f():
	A=platform.system()
	if A=='Windows':return _N
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
class KernelException(Exception):
	def __init__(B,message):
		A=message;super().__init__(A)
		if B_DEBUG:logger.debug('KernelException message');logger.debug(A)
		B.traceback_msg=A
	def get_traceback_errors(A):return A.traceback_msg
class IPythonKernel:
	async def __init__(A,api_key=_A,core_api_path=_A,django_settings_module=_A,project_folder=_A):E='***********************************************************';D=django_settings_module;C=core_api_path;B=api_key;logger.debug(E);logger.debug('Instantiate new Kernel');logger.debug(E);logger.debug(f"django_settings_module > {D}");logger.debug(f"api_key > {B}");logger.debug(f"core_api_path > {C}");A.api_key=B;A.core_api_path=C;A.workspaceVarNameArr=[];A.django_settings_module=D;A.project_folder=project_folder;A.output_queue=[];A.last_send_time=time.time();A.kernel_manager=KernelManager();await A.startup_kernel()
	async def startup_kernel(A):
		if A.django_settings_module is not _A:B=os.environ.copy();B['DJANGO_ALLOW_ASYNC_UNSAFE']='true';A.kernel_manager.start_kernel(env=B)
		else:A.kernel_manager.start_kernel()
		A.kernel_client=A.kernel_manager.client();A.kernel_client.start_channels()
		try:A.kernel_client.wait_for_ready();C=time.time();logger.debug('Ready, initialize with Django');await A.initialize_kernel();logger.debug('Kernel is init');logger.debug('--- %s seconds ---'%(time.time()-C))
		except RuntimeError:A.kernel_client.stop_channels();A.kernel_manager.shutdown_kernel()
	async def send_sync(A,websocket,data):
		A.output_queue.append(data)
		if time.time()-A.last_send_time>=SEND_INTERVAL:logger.debug(f"Send batch now Interval diff: {time.time()-A.last_send_time}");await A.send_batch(websocket)
	async def send_batch(A,websocket):
		B=websocket
		if len(A.output_queue)>0:
			logger.debug('='*20);logger.debug(f"SEND BATCH NOW {len(A.output_queue)}");logger.debug(json.dumps(A.output_queue)[:100]);logger.debug('websocket');logger.debug(B)
			if B is not _A:C={_G:1,_J:_K,'batch_output':A.output_queue};await B.send(json.dumps(C));A.output_queue=[];A.last_send_time=time.time()
	async def process_command(A,websocket,data):A.output_queue.append(data)
	def get_kernel_manager(A):return A.kernel_manager
	def get_kernel_client(A):return A.kernel_client
	async def initialize_kernel(B):
		A='import os, sys\n';A+='import django\n';A+='os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"\n'
		if B.project_folder is not _A:D=f'user_app_db_path = r"{os.path.join(B.project_folder,"app","db.sqlite3")}"\n';D+='from django.conf import settings\n';D+='user_app_name = "notebook_app"\n';D+='settings.DATABASES[user_app_name] = {"ENGINE": "django.db.backends.sqlite3", "NAME": user_app_db_path}\n';A+=D
		A+='django.setup()\n';F=os.path.dirname(__file__);E=os.path.dirname(F);G=os.path.dirname(E);C=os.path.join(E,'api');C=sparta_6fbba8ac09(C);C=Path(C).resolve()
		if B.core_api_path is not _A:A+=f'sys.path.insert(0, r"{str(G)}")\n';A+=f'sys.path.insert(0, r"{str(C)}")\n';A+=f'os.environ["api_key"] = "{B.api_key}"\n'
		if B.project_folder is not _A:A+=f'os.chdir(r"{B.project_folder}")\n'
		logger.debug('ini_code');logger.debug(A);await B.execute(A,b_debug=_E);await B.backup_venv_at_startup()
	async def backup_venv_at_startup(A):B=f'import sys, os, json\nos.environ["PATH_BK"] = os.environ["PATH"]\nos.environ["VIRTUAL_ENV_BK"] = os.environ["VIRTUAL_ENV"]\nos.environ["SYS_PATH_BK"] = json.dumps(sys.path)\n';await A.execute(B)
	async def activate_venv(C,venv_name):
		def D():
			B=sparta_a93cc5ef0f()
			if B==_N:A=f"C:\\Users\\{getpass.getuser()}\\SpartaQube\\sq_venv"
			elif B=='linux':A=os.path.expanduser('~/SpartaQube/sq_venv')
			elif B=='mac':A=os.path.expanduser('~/Library/Application Support\\SpartaQube\\sq_venv')
			A=os.path.normpath(A);os.makedirs(A,exist_ok=True);return A
		def A():return os.path.normpath(os.path.join(D(),venv_name))
		def E():
			if os.name=='nt':B=os.path.join(A(),'Scripts')
			else:B=os.path.join(A(),'bin')
			return os.path.normpath(B)
		def F():
			C='site-packages'
			if os.name=='nt':B=os.path.join(A(),'Lib',C)
			else:D=f"python{sys.version_info.major}.{sys.version_info.minor}";B=os.path.join(A(),'lib',D,C)
			return os.path.normpath(B)
		G=f'import sys, os\nos.environ["PATH"] = os.environ["PATH_BK"]\nos.environ["VIRTUAL_ENV"] = os.environ["VIRTUAL_ENV_BK"]\n';H=f'os.environ["PATH"] = r"{E()};" + os.environ["PATH"] \nsite_packages_path = r"{F()}"\nsys.path = [elem for elem in sys.path if "site-packages" not in elem] \nsys.path.insert(0, site_packages_path)\n';B=G+H;logger.debug('+'*100);logger.debug('cmd_to_execute activate VENV');logger.debug(B);logger.debug('+'*100);await C.execute(B)
	async def deactivate_venv(A):B=f'import sys, os, json\nos.environ["PATH"] = os.environ["PATH_BK"]\nos.environ["VIRTUAL_ENV"] = os.environ["VIRTUAL_ENV_BK"]\nsys.path = json.loads(os.environ["SYS_PATH_BK"])\n';await A.execute(B)
	def stop_kernel(A):A.kernel_client.stop_channels();A.kernel_manager.interrupt_kernel();A.kernel_manager.shutdown_kernel(now=True)
	async def cd_to_notebook_folder(C,notebook_path,websocket=_A):B=notebook_path;A=f"import os, sys\n";A+=f"os.chdir('{B}')\n";A+=f"sys.path.insert(0, '{B}')";await C.execute(A,websocket)
	def escape_ansi(C,line):A=re.compile('\\x1B(?:[@-Z\\\\-_]|\\[[0-?]*[ -/]*[@-~])');A=re.compile('(?:\\x1B[@-_]|[\\x80-\\x9F])[0-?]*[ -/]*[@-~]');A=re.compile('(\\x9B|\\x1B\\[)[0-?]*[ -/]*[@-~]');B='\\x1b((\\[\\??\\d+[hl])|([=<>a-kzNM78])|([\\(\\)][a-b0-2])|(\\[\\d{0,2}[ma-dgkjqi])|(\\[\\d+;\\d+[hfy]?)|(\\[;?[hf])|(#[3-68])|([01356]n)|(O[mlnp-z]?)|(/Z)|(\\d+)|(\\[\\?\\d;\\d0c)|(\\d;\\dR))';A=re.compile(B,flags=re.IGNORECASE);return A.sub('',line)
	async def execute(B,cmd,websocket=_A,cell_id=_A,b_debug=_E):
		O='resJson';N='traceback';M='/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/';I=b_debug;H='cell_id';F=cell_id;D=websocket;B.last_send_time=time.time();R=B.kernel_client.execute(cmd);J=_L;E=_A
		while J!=_M and B.kernel_client.is_alive():
			try:
				K=B.kernel_client.get_iopub_msg()
				if not _B in K:continue
				A=K[_B]
				if B_DEBUG or I:logger.debug(M);logger.debug(type(A));logger.debug(A);logger.debug(A.keys());logger.debug(M)
				if N in A:
					if B_DEBUG or I:logger.debug('TRACEBACK RAISE EXCEPTION NOW');logger.debug(A)
					P=re.compile('<ipython-input-\\d+-[0-9a-f]+>');L=[re.sub(P,'<IPY-INPUT>',strip_ansi(A))for A in A[N]];E=KernelException('\n'.join(L))
					if D is not _A:C=json.dumps({_G:-1,H:F,_J:_K,'errorMsg':'\n'.join(L)});await B.send_sync(D,C)
				if _F in A:
					if A[_F]==_O:
						E=A['text'];G=B.format_output(E);C=json.dumps({_G:1,_J:_K,_C:G,H:F})
						if B_DEBUG:logger.debug(O);logger.debug(C)
						await B.send_sync(D,C)
				if _H in A:
					E=A[_H]
					if D is not _A:
						G=B.format_output(E);C=json.dumps({_G:1,_J:_K,_C:G,H:F})
						if B_DEBUG:logger.debug(O);logger.debug(C)
						await B.send_sync(D,C)
				if _D in A:J=A[_D]
			except Exception as Q:logger.debug('Execute exception EXECUTION');logger.debug(Q)
		logger.debug('Send batch final');await B.send_batch(D);return E
	async def list_workspace_variables(C):
		N='df_columns';M='is_df';L='preview'
		def O(data,trunc_size):B=trunc_size;A=data;A=A[:B]+'...'if len(A)>B else A;return A
		P='%whos';U=C.kernel_client.execute(P);H=_L;A=[]
		while H!=_M and C.kernel_client.is_alive():
			try:
				I=C.kernel_client.get_iopub_msg()
				if not _B in I:continue
				D=I[_B]
				if _F in D:
					if D[_F]==_O:A.append(D['text'])
				if _D in D:H=D[_D]
			except Exception as F:logger.debug(F);pass
		G=await C.get_kernel_variables_memory_dict()
		if G is _A:G=dict()
		try:
			A=''.join(A).split('\n');A=A[2:-1];J=[]
			for Q in A:
				E=re.split('\\s{2,}',Q.strip())
				if len(E)>=2:K=E[0];R=E[1];S=' '.join(E[2:])if len(E)>2 else'';J.append({_F:K,_I:R,L:S,'size':G.get(K,0)})
			A=J
			for B in A:
				B['preview_display']=O(B[L],30);B[M]=_E;B[N]=json.dumps([])
				if B[_I]=='DataFrame':
					try:T=await convert_to_dataframe(C.get_workspace_variable(B[_F]),B[_F]);B[N]=json.dumps(list(T.columns));B[M]=True
					except:pass
		except Exception as F:logger.debug('Except list workspace var');logger.debug(F)
		return A
	async def get_kernel_variables_memory_dict(A):B='size_in_bytes_variables_dict';C='\nimport os, sys\ndef get_size_bytes_variables_dict():\n    # Exclude the function itself and common IPython artifacts\n    excluded_vars = {"get_size_mb", "_", "__builtins__", "__file__", "__name__", "__doc__"}\n    all_vars = {k: v for k, v in globals().items() if k not in excluded_vars and not callable(v) and not k.startswith("__")}\n    \n    variables_mem_dict = dict()\n    for var_name, obj in all_vars.items():\n        variables_mem_dict[var_name] = sys.getsizeof(obj)\n    \n    return variables_mem_dict\nsize_in_bytes_variables_dict = get_size_bytes_variables_dict()    \n';await A.execute(C,b_debug=_E);D=A.get_workspace_variable(B);await A.remove_variable_from_kernel(B);return D
	async def get_kernel_memory_size(A):B='size_in_bytes';C='\ndef get_size_bytes():\n    # Exclude the function itself and common IPython artifacts\n    excluded_vars = {"get_size_mb", "_", "__builtins__", "__file__", "__name__", "__doc__"}\n    all_vars = {k: v for k, v in globals().items() if k not in excluded_vars and not callable(v) and not k.startswith("__")}\n    \n    size_in_bytes = 0\n    for var_name, obj in all_vars.items():\n        size_in_bytes += sys.getsizeof(obj)\n    \n    return size_in_bytes\nsize_in_bytes = get_size_bytes()    \n';await A.execute(C,b_debug=_E);D=A.get_workspace_variable(B);await A.remove_variable_from_kernel(B);return D
	def sparta_c88ae94202(A,kernel_variable):
		F=f"{kernel_variable}";J=A.kernel_client.execute(F);C=_L;D=json.dumps({_G:-1})
		while C!=_M and A.kernel_client.is_alive():
			try:
				E=A.kernel_client.get_iopub_msg()
				if not _B in E:continue
				B=E[_B]
				if _H in B:G=B[_H];H=A.format_output(G);D=json.dumps({_G:1,_C:H})
				if _D in B:C=B[_D]
			except Exception as I:logger.debug('Exception get_kernel_variable_repr');logger.debug(I);pass
		return D
	def format_output(E,output):
		D='image/png';C='text/html';B='text/plain';A=output
		if isinstance(A,dict):
			if C in A:return{_C:A[C],_I:C}
			if D in A:return{_C:A[D],_I:D}
			if B in A:return{_C:A[B],_I:B}
		return{_C:A,_I:B}
	async def get_workspace_variable(A,kernel_variable):
		D=_A
		try:
			G=f"import cloudpickle\nimport base64\ntmp_sq_ans = _\nbase64.b64encode(cloudpickle.dumps({kernel_variable})).decode()";J=A.kernel_client.execute(G);E=_L
			while E!=_M and A.kernel_client.is_alive():
				try:
					F=A.kernel_client.get_iopub_msg()
					if not _B in F:continue
					B=F[_B]
					if _H in B:H=B[_H];I=A.format_output(H);D=cloudpickle.loads(base64.b64decode(I[_C]))
					if _D in B:E=B[_D]
				except Exception as C:logger.debug(C);pass
		except Exception as C:logger.debug('Exception get_workspace_variable');logger.debug(C)
		await A.execute(f"del tmp_sq_ans");await A.execute(f"del cloudpickle");await A.execute(f"del base64");return D
	async def set_workspace_variables(A,variables_dict,websocket=_A):
		for(B,C)in variables_dict.items():await A.set_workspace_variable(B,C,websocket=websocket)
	async def sparta_e7efb4ac22(A,name,value,websocket=_A):
		try:B=f'import cloudpickle\nimport base64\n{name} = cloudpickle.loads(base64.b64decode("{base64.b64encode(cloudpickle.dumps(value)).decode()}"))';await A.execute(B,websocket)
		except Exception as C:logger.debug('Exception setWorkspaceVariable');logger.debug(C)
		await A.execute(f"del cloudpickle");await A.execute(f"del base64")
	async def reset_kernel_workspace(A):B='%reset -f';await A.execute(B)
	async def remove_variable_from_kernel(A,kernel_variable):B="del globals()['"+str(kernel_variable)+"']";await A.execute(B)
	async def cloudpickle_kernel_variables(A):C='kernel_cpkl_unpicklable';B='kernel_cpkl_picklable';await A.execute('import cloudpickle');await A.execute("\nimport io\nimport cloudpickle\ndef test_picklability():\n    variables = {k: v for k, v in globals().items() if not k.startswith('_')}\n    picklable = {}\n    unpicklable = {}\n    var_not_to_pickle = ['In', 'Out', 'test_picklability']\n    \n    for var_name, var_value in variables.items():\n        if var_name in var_not_to_pickle:\n            continue\n        try:\n            # Attempt to serialize the variable\n            buffer = io.BytesIO()\n            cloudpickle.dump(var_value, buffer)\n            picklable[var_name] = buffer.getvalue()\n        except Exception as e:\n            unpicklable[var_name] = (type(var_value).__name__, str(e))\n    \n    return picklable, unpicklable\n\nkernel_cpkl_picklable, kernel_cpkl_unpicklable = test_picklability()\ndel test_picklability\n");D=await A.get_workspace_variable(B);E=await A.get_workspace_variable(C);await A.remove_variable_from_kernel(B);await A.remove_variable_from_kernel(C);return D,E
	async def execute_code(A,cmd,websocket=_A,cell_id=_A,bTimeout=_E):
		C=cell_id;B=websocket
		if bTimeout:return await A.execute_code_timeout(cmd,websocket=B,cell_id=C)
		else:return await A.execute_code_no_timeout(cmd,websocket=B,cell_id=C)
	@timeout(sparta_40d9acc6f9())
	async def execute_code_timeout(self,cmd,websocket=_A,cell_id=_A):return await self.execute(cmd,websocket=websocket,cell_id=cell_id)
	async def execute_code_no_timeout(A,cmd,websocket=_A,cell_id=_A):return await A.execute(cmd,websocket=websocket,cell_id=cell_id)
	def getLastExecutedVariable(A,websocket):
		try:B=f"import cloudpickle\nimport base64\ntmp_sq_ans = _\nbase64.b64encode(cloudpickle.dumps(tmp_sq_ans)).decode()";return cloudpickle.loads(base64.b64decode(A.format_output(A.execute(B,websocket))))
		except Exception as C:logger.debug('Excep last exec val');raise C
	def sparta_398466269c(A,nameVar):
		try:B=f"import cloudpickle\nimport base64\ntmp_sq_ans = _\nbase64.b64encode(cloudpickle.dumps({nameVar})).decode()";return cloudpickle.loads(base64.b64decode(A.format_output(A.execute(B))))
		except Exception as C:logger.debug('Exception get_kernel_variable');logger.debug(C);return
	def removeWorkspaceVariable(A,name):
		try:del A.workspaceVarNameArr[name]
		except Exception as B:logger.debug('Exception removeWorkspaceVariable');logger.debug(B)
	def getWorkspaceVariables(A):return[]