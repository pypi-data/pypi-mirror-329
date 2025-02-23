import json,base64,asyncio,subprocess,uuid,requests,pandas as pd
from subprocess import PIPE
from django.db.models import Q
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared
from project.models import ShareRights
from project.sparta_ab7a1c0e2d.sparta_9130611051 import qube_fb51653a52 as qube_fb51653a52
from project.sparta_ab7a1c0e2d.sparta_bb21f59158 import qube_a879ba9993
from project.sparta_ab7a1c0e2d.sparta_6016211a05 import qube_73b3a04f31 as qube_73b3a04f31
from project.sparta_ab7a1c0e2d.sparta_bb21f59158.qube_431d9fc3ad import Connector as Connector
def sparta_1b44efa2e6(json_data,user_obj):
	D='key';A=json_data;print('Call autocompelte api');print(A);B=A[D];E=A['api_func'];C=[]
	if E=='tv_symbols':C=sparta_a96008f93b(B)
	return{'res':1,'output':C,D:B}
def sparta_a96008f93b(key_symbol):
	F='</em>';E='<em>';B='symbol_id';G=f"https://symbol-search.tradingview.com/local_search/v3/?text={key_symbol}&hl=1&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US";C=requests.get(G)
	try:
		if int(C.status_code)==200:
			H=json.loads(C.text);D=H['symbols']
			for A in D:A[B]=A['symbol'].replace(E,'').replace(F,'');A['title']=A[B];A['subtitle']=A['description'].replace(E,'').replace(F,'');A['value']=A[B]
			return D
		return[]
	except:return[]