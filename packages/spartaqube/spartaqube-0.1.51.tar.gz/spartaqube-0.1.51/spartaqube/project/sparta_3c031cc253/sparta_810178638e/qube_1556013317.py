import json,base64,websocket
from channels.generic.websocket import WebsocketConsumer
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.sparta_ab7a1c0e2d.sparta_c744d29a89 import qube_5aed79e4f4 as qube_5aed79e4f4
class GitNotebookWS(WebsocketConsumer):
	channel_session=True;http_user_and_session=True
	def connect(A):A.accept();A.user=A.scope['user'];A.json_data_dict=dict()
	def disconnect(A,close_code):A.close()
	def sendStatusMsg(A,thisMsg):B={'res':3,'statusMsg':thisMsg};A.send(text_data=json.dumps(B))
	def receive(A,text_data):
		B=text_data;print('RECEIVE GIT INSTALL');print('text_data > ');print(B)
		if len(B)>0:C=json.loads(B);A.json_data_dict=C;D=qube_5aed79e4f4.sparta_de73672893(A,C,A.user);A.send(text_data=json.dumps(D));print('FINISH SOCKET')