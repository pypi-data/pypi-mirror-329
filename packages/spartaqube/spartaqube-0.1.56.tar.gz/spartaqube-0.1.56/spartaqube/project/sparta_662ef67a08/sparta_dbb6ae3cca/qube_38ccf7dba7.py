_F='output'
_E=False
_D=None
_C='name'
_B='utf-8'
_A='res'
import os,sys,json,ast,re,base64,uuid,hashlib,socket,cloudpickle,websocket,subprocess,threading
from random import randint
import pandas as pd
from pathlib import Path
from cryptography.fernet import Fernet
from subprocess import PIPE
from datetime import datetime,timedelta
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.cache import cache
from django.conf import settings as conf_settings
import pytz
UTC=pytz.utc
from spartaqube_app.path_mapper_obf import sparta_eb692a7fc2
from project.models import UserProfile,NewPlotApiVariables,NotebookShared,DashboardShared
from project.sparta_662ef67a08.sparta_b9c728af58 import qube_60ba9e4a49 as qube_60ba9e4a49
from project.sparta_662ef67a08.sparta_928c4c5c7e import qube_8088811bba as qube_8088811bba
from project.sparta_662ef67a08.sparta_bc02ea2c9b.qube_2ac5797abc import convert_to_dataframe,convert_dataframe_to_json,sparta_6fbba8ac09
from project.sparta_662ef67a08.sparta_bc02ea2c9b.qube_5ec6d481e9 import sparta_130c38b847,sparta_36ad9c2fb1
from project.logger_config import logger
def sparta_5a70fb16a2():keygen_fernet='spartaqube-api-key';key=keygen_fernet.encode(_B);key=hashlib.md5(key).hexdigest();key=base64.b64encode(key.encode(_B));return key.decode(_B)
def sparta_39b68376c1():keygen_fernet='spartaqube-internal-decoder-api-key';key=keygen_fernet.encode(_B);key=hashlib.md5(key).hexdigest();key=base64.b64encode(key.encode(_B));return key.decode(_B)
def sparta_4e7535d69c(f,str_to_encrypt):data_to_encrypt=str_to_encrypt.encode(_B);token=f.encrypt(data_to_encrypt).decode(_B);token=base64.b64encode(token.encode(_B)).decode(_B);return token
def sparta_f2287b01f2(api_token_id):
	if api_token_id=='public':
		try:return User.objects.filter(email='public@spartaqube.com').all()[0]
		except:return
	try:
		f_private=Fernet(sparta_39b68376c1().encode(_B));api_key=f_private.decrypt(base64.b64decode(api_token_id)).decode(_B).split('@')[1];user_profile_set=UserProfile.objects.filter(api_key=api_key,is_banned=_E).all()
		if user_profile_set.count()==1:return user_profile_set[0].user
		return
	except Exception as e:logger.debug('Could not authenticate api with error msg:');logger.debug(e);return
def sparta_7245720e20(user_obj):
	userprofile_obj=UserProfile.objects.get(user=user_obj);api_key=userprofile_obj.api_key
	if api_key is _D:api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;userprofile_obj.save()
	return api_key
async def get_api_key_async(user_obj):
	userprofile_obj=await UserProfile.objects.aget(user=user_obj);api_key=userprofile_obj.api_key
	if api_key is _D:api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;await userprofile_obj.asave()
	return api_key
def sparta_a70ad7bec7(user_obj,domain_name):api_key=sparta_7245720e20(user_obj);random_nb=str(randint(0,1000));data_to_encrypt=f"apikey@{api_key}@{random_nb}";f_private=Fernet(sparta_39b68376c1().encode(_B));private_encryption=sparta_4e7535d69c(f_private,data_to_encrypt);data_to_encrypt=f"apikey@{domain_name}@{private_encryption}";f_public=Fernet(sparta_5a70fb16a2().encode(_B));public_encryption=sparta_4e7535d69c(f_public,data_to_encrypt);return public_encryption
def sparta_8cd2676b0f(json_data,user_obj):api_key=sparta_7245720e20(user_obj);domain_name=json_data['domain'];public_encryption=sparta_a70ad7bec7(user_obj,domain_name);return{_A:1,'token':public_encryption}
def sparta_9b95caa217(json_data,user_obj):userprofile_obj=UserProfile.objects.get(user=user_obj);api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;userprofile_obj.save();return{_A:1}
def sparta_680eab35c0():plot_types=sparta_130c38b847();plot_types=sorted(plot_types,key=lambda x:x['Library'].lower(),reverse=_E);return{_A:1,'plot_types':plot_types}
def sparta_ce67d5a92e(json_data):logger.debug('DEBUG get_plot_options json_data');logger.debug(json_data);plot_type=json_data['plot_type'];plot_input_options_dict=sparta_36ad9c2fb1(plot_type);plot_input_options_dict[_A]=1;return plot_input_options_dict
def sparta_cbf24a264d(code):
	tree=ast.parse(code)
	if isinstance(tree.body[-1],ast.Expr):last_expr_node=tree.body[-1].value;last_expr_code=ast.unparse(last_expr_node);return last_expr_code
	else:return
def sparta_db5d800a30(json_data,user_obj):
	A='errorMsg';user_code_example=json_data['userCode'];resp=_D;error_msg=''
	try:
		logger.debug('EXECUTE API EXAMPLE DEBUG DEBUG DEBUG');api_key=sparta_7245720e20(user_obj);core_api_path=sparta_eb692a7fc2()['project/core/api'];ini_code='import os, sys\n';ini_code+=f'sys.path.insert(0, r"{str(core_api_path)}")\n';ini_code+='from spartaqube import Spartaqube as Spartaqube\n';ini_code+=f"Spartaqube('{api_key}')\n";user_code_example=ini_code+'\n'+user_code_example;exec(user_code_example,globals(),locals());last_expression_str=sparta_cbf24a264d(user_code_example)
		if last_expression_str is not _D:
			last_expression_output=eval(last_expression_str)
			if last_expression_output.__class__.__name__=='HTML':resp=last_expression_output.data
			else:resp=last_expression_output
			resp=json.dumps(resp);return{_A:1,'resp':resp,A:error_msg}
		return{_A:-1,A:'No output to display. You should put the variable to display as the last line of the code'}
	except Exception as e:return{_A:-1,A:str(e)}
def sparta_f6f2656d97(json_data,user_obj):
	session_id=json_data['session'];new_plot_api_variables_set=NewPlotApiVariables.objects.filter(session_id=session_id).all();logger.debug(f"gui_plot_api_variables with session_id {session_id}");logger.debug(new_plot_api_variables_set)
	if new_plot_api_variables_set.count()>0:
		new_plot_api_variables_obj=new_plot_api_variables_set[0];pickled_variables=new_plot_api_variables_obj.pickled_variables;unpickled_data=cloudpickle.loads(pickled_variables.encode('latin1'));notebook_variables=[]
		for notebook_variable in unpickled_data:
			notebook_variables_df=convert_to_dataframe(notebook_variable)
			if notebook_variables_df is not _D:0
			else:notebook_variables_df=pd.DataFrame()
			notebook_variables.append(convert_dataframe_to_json(notebook_variables_df))
		logger.debug(notebook_variables);return{_A:1,'notebook_variables':notebook_variables}
	return{_A:-1}
def sparta_a29fd6d0f1(json_data,user_obj):widget_id=json_data['widgetId'];return qube_8088811bba.sparta_a29fd6d0f1(user_obj,widget_id)
def sparta_65c622b94c(json_data,user_obj):
	api_service=json_data['api_service']
	if api_service=='get_status':output=sparta_905db380c2()
	elif api_service=='get_status_ws':return sparta_757d73806f()
	elif api_service=='get_connectors':return sparta_16e1670ece(json_data,user_obj)
	elif api_service=='get_connector_tables':return sparta_97e69af87d(json_data,user_obj)
	elif api_service=='get_data_from_connector':return sparta_b85ae9be8f(json_data,user_obj)
	elif api_service=='get_widgets':output=sparta_2a9b67445f(user_obj)
	elif api_service=='has_widget_id':return sparta_de2acc947a(json_data,user_obj)
	elif api_service=='get_widget_data':return sparta_9f68230ff7(json_data,user_obj)
	elif api_service=='get_plot_types':return sparta_130c38b847()
	return{_A:1,_F:output}
def sparta_905db380c2():return 1
def sparta_16e1670ece(json_data,user_obj):
	A='db_connectors';keys_to_retain=['connector_id',_C,'db_engine'];res_dict=qube_8088811bba.sparta_c58d36b2c6(json_data,user_obj)
	if res_dict[_A]==1:res_dict[A]=[{k:d[k]for k in keys_to_retain if k in d}for d in res_dict[A]]
	return res_dict
def sparta_97e69af87d(json_data,user_obj):res_dict=qube_8088811bba.sparta_447dd996b5(json_data,user_obj);return res_dict
def sparta_b85ae9be8f(json_data,user_obj):res_dict=qube_8088811bba.sparta_291a84b6a1(json_data,user_obj);return res_dict
def sparta_2a9b67445f(user_obj):return qube_8088811bba.sparta_2526250c49(user_obj)
def sparta_de2acc947a(json_data,user_obj):return qube_8088811bba.sparta_de2acc947a(json_data,user_obj)
def sparta_9f68230ff7(json_data,user_obj):return qube_8088811bba.sparta_dadd4d1d27(json_data,user_obj)
def sparta_4962baa945(json_data,user_obj):date_now=datetime.now().astimezone(UTC);session_id=str(uuid.uuid4());pickled_data=json_data['data'];NewPlotApiVariables.objects.create(user=user_obj,session_id=session_id,pickled_variables=pickled_data,date_created=date_now,last_update=date_now);return{_A:1,'session_id':session_id}
def sparta_0e5a44451b():return sparta_130c38b847()
def sparta_a9093a888d():cache.clear();return{_A:1}
def sparta_757d73806f():
	global is_wss_valid;is_wss_valid=_E
	try:
		api_path=sparta_eb692a7fc2()['api']
		with open(os.path.join(api_path,'app_data_asgi.json'),'r')as json_file:loaded_data_dict=json.load(json_file)
		ASGI_PORT=int(loaded_data_dict['default_port'])
	except:ASGI_PORT=5664
	logger.debug('ASGI_PORT');logger.debug(ASGI_PORT)
	def on_open(ws):global is_wss_valid;is_wss_valid=True;ws.close()
	def on_error(ws,error):global is_wss_valid;is_wss_valid=_E;ws.close()
	def on_close(ws,close_status_code,close_msg):
		try:logger.debug(f"Connection closed with code: {close_status_code}, message: {close_msg}");ws.close()
		except Exception as e:logger.debug(f"Except: {e}")
	ws=websocket.WebSocketApp(f"ws://127.0.0.1:{ASGI_PORT}/ws/statusWS",on_open=on_open,on_close=on_close);ws.run_forever()
	if ws.sock and ws.sock.connected:logger.debug('WebSocket is still connected. Attempting to close again.');ws.close()
	else:logger.debug('WebSocket is properly closed.')
	return{_A:1,_F:is_wss_valid}
def sparta_24b71954ee(json_data,user_obj):
	H='displayText';G='Plot';F='dict';E='popTitle';D='other';C='preview';B='popType';A='type';api_methods=[{_C:'Spartaqube().get_connectors()',A:1,B:F,C:'',D:'',E:'Get Connectors'},{_C:'Spartaqube().get_connector_tables("connector_id")',A:1,B:F,C:'',D:'',E:'Get Connector Tables'},{_C:'Spartaqube().get_data_from_connector("connector_id", table=None, sql_query=None, output_format=None)',A:1,B:F,C:'',D:'',E:'Get Connector Data'},{_C:'Spartaqube().get_plot_types()',A:1,B:'list',C:'',D:'',E:'Get Plot Type'},{_C:'Spartaqube().get_widgets()',A:1,B:F,C:'',D:'',E:'Get Widgets list'},{_C:'Spartaqube().iplot([var1, var2], width="100%", height=750)',A:1,B:G,C:'',D:'-1',E:'Interactive plot'},{_C:'Spartaqube().plot(\n    x:list=None, y:list=None, r:list=None, legend:list=None, labels:list=None, ohlcv:list=None, shaded_background:list=None, \n    datalabels:list=None, border:list=None, background:list=None, border_style:list=None, tooltips_title:list=None, tooltips_label:list=None,\n    chart_type="line", interactive=True, widget_id=None, title=None, title_css:dict=None, stacked:bool=False, date_format:str=None, time_range:bool=False,\n    gauge:dict=None, gauge_zones:list=None, gauge_zones_labels:list=None, gauge_zones_height:list=None,\n    dataframe:pd.DataFrame=None, dates:list=None, returns:list=None, returns_bmk:list=None,\n    options:dict=None, width=\'100%\', height=750\n)',A:1,B:G,C:'',D:'-1',H:'Spartaqube().plot(...)',E:'Programmatic plot'}];api_widgets_suggestions=[]
	if not user_obj.is_anonymous:
		api_get_widgets=sparta_2a9b67445f(user_obj)
		for widget_dict in api_get_widgets:widget_id_with_quote="'"+str(widget_dict['id'])+"'";widget_cmd=f"Spartaqube().get_widget({widget_id_with_quote})";api_widgets_suggestions.append({_C:widget_cmd,H:widget_dict[_C],E:widget_dict[_C],A:2,B:'Widget',C:widget_cmd,D:widget_dict['id']})
	autocomplete_suggestions_arr=api_methods+api_widgets_suggestions;return{_A:1,'suggestions':autocomplete_suggestions_arr}
def sparta_df67d463a0(notebook_id):
	notebook_shared_set=NotebookShared.objects.filter(is_delete=0,notebook__is_delete=0,notebook__notebook_id=notebook_id)
	if notebook_shared_set.count()>0:return notebook_shared_set[0].user
def sparta_483ff01223(dashboard_id):
	dashboard_shared_set=DashboardShared.objects.filter(is_delete=0,dashboard__is_delete=0,dashboard__dashboard_id=dashboard_id)
	if dashboard_shared_set.count()>0:return dashboard_shared_set[0].user