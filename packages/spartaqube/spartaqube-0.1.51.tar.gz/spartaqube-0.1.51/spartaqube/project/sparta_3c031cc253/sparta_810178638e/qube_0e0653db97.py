import re,json,subprocess
from channels.generic.websocket import WebsocketConsumer
from project.sparta_ab7a1c0e2d.sparta_c744d29a89 import qube_d81e305624 as qube_d81e305624
def sparta_964f1060d7(command):
	A=command
	if not A.startswith('pip install'):return False
	B='^pip install( [a-zA-Z0-9_\\-\\.]+(==|>=|<=|>|<)?[a-zA-Z0-9_\\-\\.]*)+$';return bool(re.match(B,A))
class PipInstallWS(WebsocketConsumer):
	channel_session=True;http_user_and_session=True
	def connect(A):print('Connect Now');A.accept();A.json_data_dict=dict()
	def disconnect(A,close_code=None):print('Disconnect');A.close()
	def receive(C,text_data):
		K='line';F=text_data;E='res'
		if len(F)>0:
			G=json.loads(F);H=G['pipInstallCmd'].strip();L=G['env_name'];M=qube_d81e305624.sparta_8e6ffa2799(L);N=H.replace('pip',M)
			if not sparta_964f1060d7(H):A={E:-1,'errorMsg':'Invalid syntax'};B=json.dumps(A);C.send(text_data=B);return
			I=0;J=subprocess.Popen(N,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
			try:
				for D in J.stdout:
					if'Successfully installed'in D or'Requirement already satisfied'in D:I=1
					A={E:2,K:D};B=json.dumps(A);C.send(text_data=B)
			except Exception as O:print(f"An error occurred: {O}");A={E:-1,K:D};B=json.dumps(A);C.send(text_data=B)
			J.wait()
		A={E:1,'success':I};B=json.dumps(A);C.send(text_data=B)