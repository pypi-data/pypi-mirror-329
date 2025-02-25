_A=None
import os,json,platform,websocket,threading,time,pandas as pd
from pathlib import Path
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from project.logger_config import logger
from project.sparta_3500f2f8a8.sparta_c6eb62a0d0 import qube_0ad4e25f38 as qube_0ad4e25f38
from project.sparta_662ef67a08.sparta_bc02ea2c9b import qube_2ac5797abc as qube_2ac5797abc
from project.sparta_662ef67a08.sparta_c60717777a.qube_d7b9d7ecaf import sparta_738e46c3f0
from project.sparta_662ef67a08.sparta_c60717777a.qube_4906eb6389 import sparta_35a66e6874
from project.sparta_662ef67a08.sparta_bc02ea2c9b.qube_2ac5797abc import convert_to_dataframe,convert_dataframe_to_json,sparta_6fbba8ac09
from project.sparta_662ef67a08.sparta_054f72bfca.qube_e384b55d37 import SenderKernel
from project.sparta_662ef67a08.sparta_dbb6ae3cca.qube_38ccf7dba7 import sparta_a70ad7bec7,sparta_7245720e20,get_api_key_async
class NotebookWS(AsyncWebsocketConsumer):
	channel_session=True;http_user_and_session=True
	async def connect(A):logger.debug('Connect Now');await A.accept();A.user=A.scope['user'];A.json_data_dict=dict();A.sender_kernel_obj=_A
	async def disconnect(A,close_code=_A):
		logger.debug('Disconnect')
		if A.sender_kernel_obj is not _A:A.sender_kernel_obj.zmq_close()
		await A.close()
	async def notebook_permission_code_exec(A,json_data):from project.sparta_662ef67a08.sparta_67a87b7baa import qube_a9e41d69b1 as B;return await coreNotebook.notebook_permission_code_exec(json_data)
	async def prepare_sender_kernel(A,kernel_manager_uuid):
		from project.models import KernelProcess as C;B=C.objects.filter(kernel_manager_uuid=kernel_manager_uuid)
		if await B.acount()>0:
			D=await B.afirst();E=D.port
			if A.sender_kernel_obj is _A:A.sender_kernel_obj=SenderKernel(A,E)
			A.sender_kernel_obj.zmq_connect()
	async def get_kernel_type(D,kernel_manager_uuid):
		from project.models import KernelProcess as B;A=B.objects.filter(kernel_manager_uuid=kernel_manager_uuid)
		if await A.acount()>0:C=await A.afirst();return C.type
		return 1
	async def receive(B,text_data):
		AK='kernel_variable_arr';AJ='workspace_variables_to_update';AI='repr_data';AH='raw_data';AG='cellTitleVarName';AF='execCodeTitle';AE='cellId';AD='cell_id';AC='cellCode';AB='activate_venv';AA='venv_name';A9='import json\n';t=text_data;s='updated_variables';r='output';q='defaultDashboardVars';m='assignGuiComponentVariable';l='variable';k='get_workspace_variable';j='json_data';i='value';Z='get_kernel_variable_repr';Y='code';T='errorMsg';Q='dashboardVenv';P='execute_code';N='\n';M='';K='kernel_variable';J='cmd';F='res';D='service'
		if len(t)>0:
			A=json.loads(t);logger.debug('-'*100);logger.debug(f"NOTEBOOK KERNEL json_data");logger.debug(A);E=A[D];u=A['kernelManagerUUID'];await B.prepare_sender_kernel(u);AL=await B.get_kernel_type(u)
			def W(code_to_exec,json_data):
				C=json_data;B=code_to_exec;A=A9
				if q in C:
					E=C[q]
					for(D,F)in E.items():G=F['outputDefaultValue'];A+=f'if "{D}" in globals():\n    pass\nelse:\n    {D} = {repr(G)}\n'
				H=json.dumps({i:_A,'col':-1,'row':-1});A+=f"if \"last_action_state\" in globals():\n    pass\nelse:\n    last_action_state = json.loads('{H}')\n"
				if len(A)>0:B=f"{A}\n{B}"
				return B
			async def R(json_data):
				E='projectSysPath';C=json_data
				if E in C:
					if len(C[E])>0:A=sparta_6fbba8ac09(C[E]);A=Path(A).resolve();F=f'import sys, os\nsys.path.insert(0, r"{str(A)}")\nos.chdir(r"{str(A)}")\n';await B.sender_kernel_obj.send_zmq_request({D:P,J:F})
			async def a(json_data):
				A=json_data
				if Q in A:
					if A[Q]is not _A:
						if len(A[Q])>0:C=A[Q];await B.sender_kernel_obj.send_zmq_request({D:AB,AA:C})
			if E=='init-socket'or E=='reconnect-kernel'or E=='reconnect-kernel-run-all':
				G={F:1,D:E}
				if q in A:I=W(M,A);await B.sender_kernel_obj.send_zmq_request({D:P,J:I})
				await R(A);await a(A);C=json.dumps(G);await B.send(text_data=C);return
			elif E=='disconnect':B.disconnect()
			elif E=='exec':
				R(A);AM=time.time();logger.debug('='*50);b=A[AC];I=b
				if AL==5:logger.debug('Execute for the notebook Execution Exec case');logger.debug(A);I=await B.notebook_permission_code_exec(A)
				I=W(I,A);v=False
				if b is not _A:
					if len(b)>0:
						if b[0]=='!':v=True
				if v:await B.sender_kernel_obj.send_zmq_request({D:'execute_shell',J:I,j:json.dumps(A)})
				else:await B.sender_kernel_obj.send_zmq_request({D:'execute',J:I,j:json.dumps(A)})
				try:w=sparta_738e46c3f0(A[AC])
				except:w=[]
				logger.debug('='*50);AN=time.time()-AM;C=json.dumps({F:2,D:E,'elapsed_time':round(AN,2),AD:A[AE],'updated_plot_variables':w,'input':json.dumps(A)});await B.send(text_data=C)
			elif E=='trigger-code-gui-component-input':
				R(A)
				try:
					try:c=json.loads(A[AF]);L=N.join([A[Y]for A in c])
					except:L=M
					AO=json.loads(A['execCodeInput']);x=N.join([A[Y]for A in AO]);U=W(x,A);U+=N+L;await B.sender_kernel_obj.send_zmq_request({D:P,J:U});V=sparta_738e46c3f0(x);y=A['guiInputVarName'];AP=A['guiOutputVarName'];AQ=A[AG];n=[y,AP,AQ];X=[]
					for S in n:
						try:O=await B.sender_kernel_obj.send_zmq_request({D:Z,K:S})
						except:O=json.dumps({F:1,r:M})
						o=convert_dataframe_to_json(convert_to_dataframe(await B.sender_kernel_obj.send_zmq_request({D:k,K:S}),y));X.append({l:S,AH:o,AI:O})
				except Exception as H:C=json.dumps({F:-1,D:E,T:str(H)});logger.debug('Error',C);await B.send(text_data=C);return
				C=json.dumps({F:1,D:E,s:V,AJ:X});await B.send(text_data=C)
			elif E=='trigger-code-gui-component-output':
				R(A)
				try:
					z=M;d=M
					if m in A:e=A[m];A0=sparta_35a66e6874(e);z=A0['assign_state_variable'];d=A0['assign_code']
					AR=json.loads(A['execCodeOutput']);A1=N.join([A[Y]for A in AR]);U=d+N;U+=z+N;U+=A1;await B.sender_kernel_obj.send_zmq_request({D:P,J:U});V=sparta_738e46c3f0(A1)
					try:V.append(A[m][l])
					except Exception as H:pass
				except Exception as H:C=json.dumps({F:-1,D:E,T:str(H)});await B.send(text_data=C);return
				C=json.dumps({F:1,D:E,s:V});await B.send(text_data=C)
			elif E=='assign-kernel-variable-from-gui':
				try:e=A[m];AS=e[i];d=f"{e[l]} = {AS}";await B.sender_kernel_obj.send_zmq_request({D:P,J:d})
				except Exception as H:C=json.dumps({F:-1,D:E,T:str(H)});await B.send(text_data=C);return
				C=json.dumps({F:1,D:E});await B.send(text_data=C)
			elif E=='exec-main-dashboard-notebook-init':
				await R(A);await a(A);I=A['dashboardFullCode'];I=W(I,A)
				try:await B.sender_kernel_obj.send_zmq_request({D:P,J:I},b_send_websocket_msg=False)
				except Exception as H:C=json.dumps({F:-1,D:E,T:str(H)});await B.send(text_data=C);return
				A2=A['plotDBRawVariablesList'];AT=A2;A3=[];A4=[]
				for p in A2:
					try:A3.append(convert_dataframe_to_json(convert_to_dataframe(await B.sender_kernel_obj.send_zmq_request({D:k,K:p}),p)));A4.append(await B.sender_kernel_obj.send_zmq_request({D:Z,K:p}))
					except Exception as H:logger.debug('Except get var');logger.debug(H)
				C=json.dumps({F:1,D:E,'variables_names':AT,'variables_raw':A3,'variables_repr':A4});await B.send(text_data=C)
			elif E=='trigger-action-plot-db':
				logger.debug('TRIGGER CODE ACTION PLOTDB');logger.debug(A)
				try:
					f=A9;f+=f"last_action_state = json.loads('{A['actionDict']}')\n"
					try:g=json.loads(A['triggerCode']);g=N.join([A[Y]for A in c])
					except:g=M
					f+=N+g;logger.debug('cmd to execute');logger.debug('cmd_to_exec');logger.debug(f);await B.sender_kernel_obj.send_zmq_request({D:P,J:f});V=sparta_738e46c3f0(g)
				except Exception as H:C=json.dumps({F:-1,D:E,T:str(H)});await B.send(text_data=C);return
				C=json.dumps({F:1,D:E,s:V});await B.send(text_data=C)
			elif E=='dynamic-title':
				try:c=json.loads(A[AF]);L=N.join([A[Y]for A in c])
				except:L=M
				if len(L)>0:
					L=W(L,A);await R(A);await a(A)
					try:
						await B.sender_kernel_obj.send_zmq_request({D:P,J:L});A5=A[AG];n=[A5];X=[]
						for S in n:
							try:O=await B.sender_kernel_obj.send_zmq_request({D:Z,K:S})
							except:O=json.dumps({F:1,r:M})
							o=convert_dataframe_to_json(convert_to_dataframe(await B.sender_kernel_obj.send_zmq_request({D:k,K:S}),A5));X.append({l:S,AH:o,AI:O})
						C=json.dumps({F:1,D:E,AJ:X});await B.send(text_data=C)
					except Exception as H:C=json.dumps({F:-1,D:E,T:str(H)});logger.debug('Error',C);logger.debug(L);await B.send(text_data=C);return
			elif E=='reset':await B.sender_kernel_obj.send_zmq_request({D:'reset_kernel_workspace'});await a(A);G={F:1,D:E};C=json.dumps(G);await B.send(text_data=C)
			elif E=='workspace-list':AU=await B.sender_kernel_obj.send_zmq_request({D:'list_workspace_variables'});G={F:1,D:E,'workspace_variables':AU};G.update(A);C=json.dumps(G);await B.send(text_data=C)
			elif E=='workspace-get-variable-as-df':
				A6=[];A7=[];A8=[]
				for h in A[AK]:
					AV=await B.sender_kernel_obj.send_zmq_request({D:k,K:h});AW=convert_to_dataframe(AV,variable_name=h)
					try:A6.append(convert_dataframe_to_json(AW));A7.append(h)
					except:pass
					try:O=await B.sender_kernel_obj.send_zmq_request({D:Z,K:h})
					except:O=json.dumps({F:1,r:M})
					A8.append(O)
				G={F:1,D:E,AK:A7,'workspace_variable_arr':A6,'kernel_variable_repr_arr':A8};C=json.dumps(G);await B.send(text_data=C)
			elif E=='workspace-get-variable'or E=='workspace-get-variable-preview':AX=await B.sender_kernel_obj.send_zmq_request({D:Z,K:A[K]});G={F:1,D:E,AD:A.get(AE,_A),'workspace_variable':AX};C=json.dumps(G);await B.send(text_data=C)
			elif E=='workspace-set-variable-from-datasource':
				if i in list(A.keys()):await B.sender_kernel_obj.send_zmq_request({D:'set_workspace_variable_from_datasource',j:json.dumps(A)});G={F:1,D:E};C=json.dumps(G);await B.send(text_data=C)
			elif E=='workspace-set-variable':
				if i in list(A.keys()):await B.sender_kernel_obj.send_zmq_request({D:'set_workspace_variable',j:json.dumps(A)});G={F:1,D:E};C=json.dumps(G);await B.send(text_data=C)
			elif E=='set-sys-path-import':
				if'projectPath'in A:await R(A)
				G={F:1,D:E};C=json.dumps(G);await B.send(text_data=C)
			elif E=='set-kernel-venv':
				if Q in A:
					if A[Q]is not _A:
						if len(A[Q])>0:AY=A[Q];await B.sender_kernel_obj.send_zmq_request({D:AB,AA:AY})
				G={F:1,D:E};C=json.dumps(G);await B.send(text_data=C)
			elif E=='deactivate-venv':await B.sender_kernel_obj.send_zmq_request({D:'deactivate_venv'});G={F:1,D:E};C=json.dumps(G);await B.send(text_data=C)
			elif E=='get-widget-iframe':
				logger.debug('Deal with iframe here');from IPython.core.display import display,HTML;import warnings as AZ;AZ.filterwarnings('ignore',message='Consider using IPython.display.IFrame instead',category=UserWarning)
				try:Aa=A['widget_id'];Ab=await get_api_key_async(B.user);Ac=await sync_to_async(lambda:HTML(f'<iframe src="/plot-widget/{Aa}/{Ab}" width="100%" height="500" frameborder="0" allow="clipboard-write"></iframe>').data)();G={F:1,D:E,'widget_iframe':Ac};C=json.dumps(G);await B.send(text_data=C)
				except Exception as H:G={F:-1,T:str(H)};C=json.dumps(G);await B.send(text_data=C)