_B=True
_A=None
import os,json,platform,websocket,threading,time,pandas as pd
from pathlib import Path
from django.conf import settings
from project.sparta_662ef67a08.sparta_c60717777a.qube_76e4aadc41 import IPythonKernel as IPythonKernel
from project.sparta_662ef67a08.sparta_c60717777a.qube_d7b9d7ecaf import sparta_738e46c3f0
from project.sparta_662ef67a08.sparta_c60717777a.qube_4906eb6389 import sparta_35a66e6874
from project.sparta_662ef67a08.sparta_bc02ea2c9b.qube_2ac5797abc import convert_to_dataframe,convert_dataframe_to_json,sparta_6fbba8ac09
IS_WINDOWS=False
if platform.system()=='Windows':IS_WINDOWS=_B
from channels.generic.websocket import WebsocketConsumer
from project.sparta_3500f2f8a8.sparta_c6eb62a0d0 import qube_0ad4e25f38 as qube_0ad4e25f38
from project.sparta_662ef67a08.sparta_bc02ea2c9b import qube_2ac5797abc as qube_2ac5797abc
from project.sparta_662ef67a08.sparta_dbb6ae3cca.qube_38ccf7dba7 import sparta_a70ad7bec7,sparta_7245720e20
from project.logger_config import logger
class NotebookWS(WebsocketConsumer):
	channel_session=_B;http_user_and_session=_B
	def connect(A):logger.debug('Connect Now');A.accept();A.user=A.scope['user'];A.json_data_dict=dict()
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
	def receive(D,text_data):
		AF='kernel_variable_arr';AE='workspace_variables_to_update';AD='repr_data';AC='raw_data';AB='cellTitleVarName';AA='execCodeTitle';A9='cell_id';A8='cellCode';A7='import json\n';r=text_data;q='updated_variables';p='output';o='defaultDashboardVars';i='assignGuiComponentVariable';h='variable';g='cellId';X='code';U='value';P='dashboardVenv';O='errorMsg';M='\n';L='';H='service';E='res'
		if len(r)>0:
			A=json.loads(r);logger.debug('-'*100);logger.debug(f"NOTEBOOK KERNEL json_data");logger.debug(A);C=A[H];s=A['kernelManagerUUID'];F=D.get_kernel_obj(s);AG=D.get_kernel_type(s)
			if F is _A:G={E:-1000,O:'Kernel lost, not found'};B=json.dumps(G);D.send(text_data=B);return
			def V(code_to_exec,json_data):
				C=json_data;B=code_to_exec;A=A7
				if o in C:
					E=C[o]
					for(D,F)in E.items():G=F['outputDefaultValue'];A+=f'if "{D}" in globals():\n    pass\nelse:\n    {D} = {repr(G)}\n'
				H=json.dumps({U:_A,'col':-1,'row':-1});A+=f"if \"last_action_state\" in globals():\n    pass\nelse:\n    last_action_state = json.loads('{H}')\n"
				if len(A)>0:B=f"{A}\n{B}"
				return B
			def Q(json_data):
				C='projectSysPath';B=json_data
				if C in B:
					if len(B[C])>0:A=sparta_6fbba8ac09(B[C]);A=Path(A).resolve();D=f'import sys, os\nsys.path.insert(0, r"{str(A)}")\nos.chdir(r"{str(A)}")\n';F.execute_code(D)
			def Y(json_data):
				A=json_data
				if P in A:
					if A[P]is not _A:
						if len(A[P])>0:B=A[P];F.activate_venv(B)
			if C=='init-socket'or C=='reconnect-kernel'or C=='reconnect-kernel-run-all':
				G={E:1,H:C}
				if o in A:J=V(L,A);F.execute_code(J)
				Q(A);Y(A);B=json.dumps(G);D.send(text_data=B);return
			elif C=='disconnect':D.disconnect()
			elif C=='exec':
				Q(A);AH=time.time();logger.debug('='*50);Z=A[A8];J=Z
				if AG==5:logger.debug('Execute for the notebook Execution Exec case');logger.debug(A);J=D.notebook_permission_code_exec(A)
				J=V(J,A);t=False
				if Z is not _A:
					if len(Z)>0:
						if Z[0]=='!':t=_B
				if t:F.execute_shell(J,websocket=D,cell_id=A[g])
				else:F.execute(J,websocket=D,cell_id=A[g])
				try:u=sparta_738e46c3f0(A[A8])
				except:u=[]
				logger.debug('='*50);AI=time.time()-AH;B=json.dumps({E:2,H:C,'elapsed_time':round(AI,2),A9:A[g],'updated_plot_variables':u,'input':json.dumps(A)});D.send(text_data=B)
			elif C=='trigger-code-gui-component-input':
				Q(A)
				try:
					try:a=json.loads(A[AA]);K=M.join([A[X]for A in a])
					except:K=L
					AJ=json.loads(A['execCodeInput']);v=M.join([A[X]for A in AJ]);S=V(v,A);S+=M+K;F.execute_code(S);T=sparta_738e46c3f0(v);w=A['guiInputVarName'];AK=A['guiOutputVarName'];AL=A[AB];j=[w,AK,AL];W=[]
					for R in j:
						try:N=F.get_kernel_variable_repr(kernel_variable=R)
						except:N=json.dumps({E:1,p:L})
						k=convert_dataframe_to_json(convert_to_dataframe(F.get_workspace_variable(kernel_variable=R),w));W.append({h:R,AC:k,AD:N})
				except Exception as I:B=json.dumps({E:-1,H:C,O:str(I)});logger.debug('Error',B);D.send(text_data=B);return
				B=json.dumps({E:1,H:C,q:T,AE:W});D.send(text_data=B)
			elif C=='trigger-code-gui-component-output':
				Q(A)
				try:
					x=L;b=L
					if i in A:c=A[i];y=sparta_35a66e6874(c);x=y['assign_state_variable'];b=y['assign_code']
					AM=json.loads(A['execCodeOutput']);z=M.join([A[X]for A in AM]);S=b+M;S+=x+M;S+=z;F.execute_code(S);T=sparta_738e46c3f0(z)
					try:T.append(A[i][h])
					except Exception as I:pass
				except Exception as I:B=json.dumps({E:-1,H:C,O:str(I)});D.send(text_data=B);return
				B=json.dumps({E:1,H:C,q:T});D.send(text_data=B)
			elif C=='assign-kernel-variable-from-gui':
				try:c=A[i];AN=c[U];b=f"{c[h]} = {AN}";F.execute_code(b)
				except Exception as I:B=json.dumps({E:-1,H:C,O:str(I)});D.send(text_data=B);return
				B=json.dumps({E:1,H:C});D.send(text_data=B)
			elif C=='exec-main-dashboard-notebook-init':
				Q(A);Y(A);J=A['dashboardFullCode'];J=V(J,A)
				try:F.execute_code(J)
				except Exception as I:B=json.dumps({E:-1,H:C,O:str(I)});D.send(text_data=B);return
				A0=A['plotDBRawVariablesList'];AO=A0;A1=[];A2=[]
				for l in A0:
					try:A1.append(convert_dataframe_to_json(convert_to_dataframe(F.get_workspace_variable(kernel_variable=l),l)));A2.append(F.get_kernel_variable_repr(kernel_variable=l))
					except Exception as I:logger.debug('Except get var');logger.debug(I)
				B=json.dumps({E:1,H:C,'variables_names':AO,'variables_raw':A1,'variables_repr':A2});D.send(text_data=B)
			elif C=='trigger-action-plot-db':
				logger.debug('TRIGGER CODE ACTION PLOTDB');logger.debug(A)
				try:
					d=A7;d+=f"last_action_state = json.loads('{A['actionDict']}')\n"
					try:e=json.loads(A['triggerCode']);e=M.join([A[X]for A in a])
					except:e=L
					d+=M+e;logger.debug('cmd to execute');logger.debug('cmd_to_exec');logger.debug(d);F.execute_code(d);T=sparta_738e46c3f0(e)
				except Exception as I:B=json.dumps({E:-1,H:C,O:str(I)});D.send(text_data=B);return
				B=json.dumps({E:1,H:C,q:T});D.send(text_data=B)
			elif C=='dynamic-title':
				try:a=json.loads(A[AA]);K=M.join([A[X]for A in a])
				except:K=L
				if len(K)>0:
					K=V(K,A);Q(A);Y(A)
					try:
						F.execute_code(K);A3=A[AB];j=[A3];W=[]
						for R in j:
							try:N=F.get_kernel_variable_repr(kernel_variable=R)
							except:N=json.dumps({E:1,p:L})
							k=convert_dataframe_to_json(convert_to_dataframe(F.get_workspace_variable(kernel_variable=R),A3));W.append({h:R,AC:k,AD:N})
						B=json.dumps({E:1,H:C,AE:W});D.send(text_data=B)
					except Exception as I:B=json.dumps({E:-1,H:C,O:str(I)});logger.debug('Error',B);logger.debug(K);D.send(text_data=B);return
			elif C=='reset':F.reset_kernel_workspace();Y(A);G={E:1,H:C};B=json.dumps(G);D.send(text_data=B)
			elif C=='workspace-list':AP=F.list_workspace_variables();G={E:1,H:C,'workspace_variables':AP};G.update(A);B=json.dumps(G);D.send(text_data=B)
			elif C=='workspace-get-variable-as-df':
				A4=[];A5=[];A6=[]
				for f in A[AF]:
					AQ=F.get_workspace_variable(kernel_variable=f);AR=convert_to_dataframe(AQ,variable_name=f)
					try:A4.append(convert_dataframe_to_json(AR));A5.append(f)
					except:pass
					try:N=F.get_kernel_variable_repr(kernel_variable=f)
					except:N=json.dumps({E:1,p:L})
					A6.append(N)
				G={E:1,H:C,AF:A5,'workspace_variable_arr':A4,'kernel_variable_repr_arr':A6};B=json.dumps(G);D.send(text_data=B)
			elif C=='workspace-get-variable'or C=='workspace-get-variable-preview':AS=F.get_kernel_variable_repr(kernel_variable=A['kernel_variable']);G={E:1,H:C,A9:A.get(g,_A),'workspace_variable':AS};B=json.dumps(G);D.send(text_data=B)
			elif C=='workspace-set-variable-from-datasource':
				if U in list(A.keys()):m=json.loads(A[U]);AT=pd.DataFrame(m['data'],columns=m['columns'],index=m['index']);F.set_workspace_variable(name=A['name'],value=AT);G={E:1,H:C};B=json.dumps(G);D.send(text_data=B)
			elif C=='workspace-set-variable':
				if U in list(A.keys()):F.set_workspace_variable(name=A['name'],value=json.loads(A[U]));G={E:1,H:C};B=json.dumps(G);D.send(text_data=B)
			elif C=='set-sys-path-import':
				if'projectPath'in A:Q(A)
				G={E:1,H:C};B=json.dumps(G);D.send(text_data=B)
			elif C=='set-kernel-venv':
				if P in A:
					if A[P]is not _A:
						if len(A[P])>0:AU=A[P];F.activate_venv(AU)
				G={E:1,H:C};B=json.dumps(G);D.send(text_data=B)
			elif C=='deactivate-venv':F.deactivate_venv();G={E:1,H:C};B=json.dumps(G);D.send(text_data=B)
			elif C=='get-widget-iframe':
				from IPython.core.display import display,HTML;import warnings as AV;AV.filterwarnings('ignore',message='Consider using IPython.display.IFrame instead',category=UserWarning)
				try:AW=A['widget_id'];AX=sparta_7245720e20(D.user);n=HTML(f'<iframe src="/plot-widget/{AW}/{AX}" width="100%" height="500" frameborder="0" allow="clipboard-write"></iframe>');n=n.data;G={E:1,H:C,'widget_iframe':n};B=json.dumps(G);D.send(text_data=B)
				except Exception as I:G={E:-1,O:str(I)};B=json.dumps(G);D.send(text_data=B)