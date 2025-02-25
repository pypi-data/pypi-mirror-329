_A=None
import os,json,platform,websocket,threading,time,pandas as pd
from pathlib import Path
from django.conf import settings
from project.sparta_662ef67a08.sparta_c60717777a.qube_76e4aadc41 import IPythonKernel as IPythonKernel
from project.sparta_662ef67a08.sparta_c60717777a.qube_d7b9d7ecaf import sparta_738e46c3f0
from project.sparta_662ef67a08.sparta_c60717777a.qube_4906eb6389 import sparta_35a66e6874
from project.sparta_662ef67a08.sparta_bc02ea2c9b.qube_2ac5797abc import convert_to_dataframe,convert_dataframe_to_json,sparta_6fbba8ac09
from project.logger_config import logger
IS_WINDOWS=False
if platform.system()=='Windows':IS_WINDOWS=True
from channels.generic.websocket import AsyncWebsocketConsumer
from project.sparta_3500f2f8a8.sparta_c6eb62a0d0 import qube_0ad4e25f38 as qube_0ad4e25f38
from project.sparta_662ef67a08.sparta_bc02ea2c9b import qube_2ac5797abc as qube_2ac5797abc
from project.sparta_662ef67a08.sparta_dbb6ae3cca.qube_38ccf7dba7 import sparta_a70ad7bec7,sparta_7245720e20
class NotebookWS(AsyncWebsocketConsumer):
	channel_session=True;http_user_and_session=True
	async def connect(A):logger.debug('Connect Now');await A.accept();A.user=A.scope['user'];A.json_data_dict=dict()
	def disconnect(A,close_code=_A):logger.debug('Disconnect')
	def get_kernel_obj(C,kernel_manager_uuid):
		A=kernel_manager_uuid
		if A in settings.GLOBAL_KERNEL_MANAGER:
			B=settings.GLOBAL_KERNEL_MANAGER[A]
			if B.user==C.user:return B.ipython_kernel
	def get_kernel_type(C,kernel_manager_uuid):
		A=kernel_manager_uuid
		if A in settings.GLOBAL_KERNEL_MANAGER:
			B=settings.GLOBAL_KERNEL_MANAGER[A]
			if B.user==C.user:return B.type
		return-1
	def notebook_permission_code_exec(B,json_data):from project.sparta_662ef67a08.sparta_67a87b7baa import qube_a9e41d69b1 as A;return A.notebook_permission_code_exec(json_data)
	async def receive(D,text_data):
		AD='kernel_variable_arr';AC='workspace_variables_to_update';AB='repr_data';AA='raw_data';A9='cellTitleVarName';A8='execCodeTitle';A7='cell_id';A6='cellCode';A5='import json\n';q=text_data;p='updated_variables';o='output';n='cellId';m='defaultDashboardVars';g='assignGuiComponentVariable';f='variable';X='code';U='value';P='dashboardVenv';O='errorMsg';M='\n';L='';H='service';E='res'
		if len(q)>0:
			A=json.loads(q);logger.debug('-'*100);logger.debug(f"NOTEBOOK KERNEL json_data");logger.debug(A);C=A[H];r=A['kernelManagerUUID'];F=D.get_kernel_obj(r);AE=D.get_kernel_type(r)
			if F is _A:G={E:-1000,O:'Kernel lost, not found'};B=json.dumps(G);await D.send(text_data=B);return
			def V(code_to_exec,json_data):
				C=json_data;B=code_to_exec;A=A5
				if m in C:
					E=C[m]
					for(D,F)in E.items():G=F['outputDefaultValue'];A+=f'if "{D}" in globals():\n    pass\nelse:\n    {D} = {repr(G)}\n'
				H=json.dumps({U:_A,'col':-1,'row':-1});A+=f"if \"last_action_state\" in globals():\n    pass\nelse:\n    last_action_state = json.loads('{H}')\n"
				if len(A)>0:B=f"{A}\n{B}"
				return B
			async def Q(json_data):
				C='projectSysPath';B=json_data
				if C in B:
					if len(B[C])>0:A=sparta_6fbba8ac09(B[C]);A=Path(A).resolve();D=f'import sys, os\nsys.path.insert(0, r"{str(A)}")\nos.chdir(r"{str(A)}")\n';await F.execute_code(D)
			async def Y(json_data):
				A=json_data
				if P in A:
					if A[P]is not _A:
						if len(A[P])>0:B=A[P];await F.activate_venv(B)
			if C=='init-socket'or C=='reconnect-kernel'or C=='reconnect-kernel-run-all':
				G={E:1,H:C}
				if m in A:J=V(L,A);await F.execute_code(J)
				await Q(A);await Y(A);B=json.dumps(G);await D.send(text_data=B);return
			elif C=='disconnect':await D.disconnect()
			elif C=='exec':
				await Q(A);AF=time.time();logger.debug('='*50);J=A[A6]
				if AE==5:logger.debug('Execute for the notebook Execution Exec case');logger.debug(A);J=D.notebook_permission_code_exec(A)
				J=V(J,A);await F.execute(J,websocket=D,cell_id=A[n])
				try:s=sparta_738e46c3f0(A[A6])
				except:s=[]
				logger.debug('='*50);AG=time.time()-AF;B=json.dumps({E:2,H:C,'elapsed_time':round(AG,2),A7:A[n],'updated_plot_variables':s,'input':json.dumps(A)});await D.send(text_data=B)
			elif C=='trigger-code-gui-component-input':
				await Q(A)
				try:
					try:Z=json.loads(A[A8]);K=M.join([A[X]for A in Z])
					except:K=L
					AH=json.loads(A['execCodeInput']);t=M.join([A[X]for A in AH]);S=V(t,A);S+=M+K;F.execute_code(S);T=sparta_738e46c3f0(t);u=A['guiInputVarName'];AI=A['guiOutputVarName'];AJ=A[A9];h=[u,AI,AJ];W=[]
					for R in h:
						try:N=F.get_kernel_variable_repr(kernel_variable=R)
						except:N=json.dumps({E:1,o:L})
						i=await convert_dataframe_to_json(convert_to_dataframe(F.get_workspace_variable(kernel_variable=R),u));W.append({f:R,AA:i,AB:N})
				except Exception as I:B=json.dumps({E:-1,H:C,O:str(I)});logger.debug('Error',B);await D.send(text_data=B);return
				B=json.dumps({E:1,H:C,p:T,AC:W});await D.send(text_data=B)
			elif C=='trigger-code-gui-component-output':
				Q(A)
				try:
					v=L;a=L
					if g in A:b=A[g];w=sparta_35a66e6874(b);v=w['assign_state_variable'];a=w['assign_code']
					AK=json.loads(A['execCodeOutput']);x=M.join([A[X]for A in AK]);S=a+M;S+=v+M;S+=x;await F.execute_code(S);T=sparta_738e46c3f0(x)
					try:T.append(A[g][f])
					except Exception as I:pass
				except Exception as I:B=json.dumps({E:-1,H:C,O:str(I)});await D.send(text_data=B);return
				B=json.dumps({E:1,H:C,p:T});await D.send(text_data=B)
			elif C=='assign-kernel-variable-from-gui':
				try:b=A[g];AL=b[U];a=f"{b[f]} = {AL}";await F.execute_code(a)
				except Exception as I:B=json.dumps({E:-1,H:C,O:str(I)});await D.send(text_data=B);return
				B=json.dumps({E:1,H:C});await D.send(text_data=B)
			elif C=='exec-main-dashboard-notebook-init':
				await Q(A);await Y(A);J=A['dashboardFullCode'];J=V(J,A)
				try:await F.execute_code(J)
				except Exception as I:B=json.dumps({E:-1,H:C,O:str(I)});await D.send(text_data=B);return
				y=A['plotDBRawVariablesList'];AM=y;z=[];A0=[]
				for j in y:
					try:z.append(convert_dataframe_to_json(convert_to_dataframe(await F.get_workspace_variable(kernel_variable=j),j)));A0.append(await F.get_kernel_variable_repr(kernel_variable=j))
					except Exception as I:logger.debug('Except get var');logger.debug(I)
				B=json.dumps({E:1,H:C,'variables_names':AM,'variables_raw':z,'variables_repr':A0});await D.send(text_data=B)
			elif C=='trigger-action-plot-db':
				logger.debug('TRIGGER CODE ACTION PLOTDB');logger.debug(A)
				try:
					c=A5;c+=f"last_action_state = json.loads('{A['actionDict']}')\n"
					try:d=json.loads(A['triggerCode']);d=M.join([A[X]for A in Z])
					except:d=L
					c+=M+d;logger.debug('cmd to execute');logger.debug('cmd_to_exec');logger.debug(c);await F.execute_code(c);T=sparta_738e46c3f0(d)
				except Exception as I:B=json.dumps({E:-1,H:C,O:str(I)});await D.send(text_data=B);return
				B=json.dumps({E:1,H:C,p:T});await D.send(text_data=B)
			elif C=='dynamic-title':
				try:Z=json.loads(A[A8]);K=M.join([A[X]for A in Z])
				except:K=L
				if len(K)>0:
					K=V(K,A);await Q(A);await Y(A)
					try:
						await F.execute_code(K);A1=A[A9];h=[A1];W=[]
						for R in h:
							try:N=await F.get_kernel_variable_repr(kernel_variable=R)
							except:N=json.dumps({E:1,o:L})
							i=convert_dataframe_to_json(convert_to_dataframe(await F.get_workspace_variable(kernel_variable=R),A1));W.append({f:R,AA:i,AB:N})
						B=json.dumps({E:1,H:C,AC:W});await D.send(text_data=B)
					except Exception as I:B=json.dumps({E:-1,H:C,O:str(I)});logger.debug('Error',B);logger.debug(K);await D.send(text_data=B);return
			elif C=='reset':await F.reset_kernel_workspace();await Y(A);G={E:1,H:C};B=json.dumps(G);await D.send(text_data=B)
			elif C=='workspace-list':AN=await F.list_workspace_variables();G={E:1,H:C,'workspace_variables':AN};G.update(A);B=json.dumps(G);await D.send(text_data=B)
			elif C=='workspace-get-variable-as-df':
				A2=[];A3=[];A4=[]
				for e in A[AD]:
					AO=await F.get_workspace_variable(kernel_variable=e);AP=convert_to_dataframe(AO,variable_name=e)
					try:A2.append(convert_dataframe_to_json(AP));A3.append(e)
					except:pass
					try:N=await F.get_kernel_variable_repr(kernel_variable=e)
					except:N=json.dumps({E:1,o:L})
					A4.append(N)
				G={E:1,H:C,AD:A3,'workspace_variable_arr':A2,'kernel_variable_repr_arr':A4};B=json.dumps(G);await D.send(text_data=B)
			elif C=='workspace-get-variable'or C=='workspace-get-variable-preview':AQ=await F.get_kernel_variable_repr(kernel_variable=A['kernel_variable']);G={E:1,H:C,A7:A.get(n,_A),'workspace_variable':AQ};B=json.dumps(G);await D.send(text_data=B)
			elif C=='workspace-set-variable-from-datasource':
				if U in list(A.keys()):k=json.loads(A[U]);AR=pd.DataFrame(k['data'],columns=k['columns'],index=k['index']);await F.set_workspace_variable(name=A['name'],value=AR);G={E:1,H:C};B=json.dumps(G);await D.send(text_data=B)
			elif C=='workspace-set-variable':
				if U in list(A.keys()):await F.set_workspace_variable(name=A['name'],value=json.loads(A[U]));G={E:1,H:C};B=json.dumps(G);await D.send(text_data=B)
			elif C=='set-sys-path-import':
				if'projectPath'in A:await Q(A)
				G={E:1,H:C};B=json.dumps(G);await D.send(text_data=B)
			elif C=='set-kernel-venv':
				if P in A:
					if A[P]is not _A:
						if len(A[P])>0:AS=A[P];await F.activate_venv(AS)
				G={E:1,H:C};B=json.dumps(G);await D.send(text_data=B)
			elif C=='deactivate-venv':await F.deactivate_venv();G={E:1,H:C};B=json.dumps(G);await D.send(text_data=B)
			elif C=='get-widget-iframe':
				from IPython.core.display import display,HTML
				try:AT=A['widget_id'];AU=sparta_7245720e20(D.user);l=HTML(f'<iframe src="/plot-widget/{AT}/{AU}" width="100%" height="500" frameborder="0" allow="clipboard-write"></iframe>');l=l.data;G={E:1,H:C,'widget_iframe':l};B=json.dumps(G);await D.send(text_data=B)
				except Exception as I:G={E:-1,O:str(I)};B=json.dumps(G);await D.send(text_data=B)