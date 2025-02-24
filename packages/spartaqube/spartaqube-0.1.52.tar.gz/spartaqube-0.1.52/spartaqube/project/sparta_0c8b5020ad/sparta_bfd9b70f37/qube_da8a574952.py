import json,base64,asyncio,subprocess,uuid,requests,pandas as pd
from subprocess import PIPE
from django.db.models import Q
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared
from project.models import ShareRights
from project.sparta_0c8b5020ad.sparta_da6af08d87 import qube_c77b125770 as qube_c77b125770
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9 import qube_9f21eab4ac
from project.sparta_0c8b5020ad.sparta_bf728a6b22 import qube_29312111b8 as qube_29312111b8
from project.sparta_0c8b5020ad.sparta_78ee0f1ac9.qube_ae890d8119 import Connector as Connector
from project.logger_config import logger
def sparta_f04fe354c7(json_data,user_obj):
	D='key';A=json_data;logger.debug('Call autocompelte api');logger.debug(A);B=A[D];E=A['api_func'];C=[]
	if E=='tv_symbols':C=sparta_17c275c80d(B)
	return{'res':1,'output':C,D:B}
def sparta_17c275c80d(key_symbol):
	F='</em>';E='<em>';B='symbol_id';G=f"https://symbol-search.tradingview.com/local_search/v3/?text={key_symbol}&hl=1&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US";C=requests.get(G)
	try:
		if int(C.status_code)==200:
			H=json.loads(C.text);D=H['symbols']
			for A in D:A[B]=A['symbol'].replace(E,'').replace(F,'');A['title']=A[B];A['subtitle']=A['description'].replace(E,'').replace(F,'');A['value']=A[B]
			return D
		return[]
	except:return[]