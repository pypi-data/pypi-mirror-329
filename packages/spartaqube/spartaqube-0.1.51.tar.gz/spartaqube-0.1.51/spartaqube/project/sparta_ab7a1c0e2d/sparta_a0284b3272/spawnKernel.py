import zmq,json,sys,os,sys
current_path=os.path.dirname(__file__)
core_path=os.path.dirname(current_path)
project_path=os.path.dirname(core_path)
main_path=os.path.dirname(project_path)
sys.path.insert(0,main_path)
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE']='true'
os.chdir(main_path)
os.environ['DJANGO_SETTINGS_MODULE']='spartaqube_app.settings'
from project.sparta_ab7a1c0e2d.sparta_e9bf664aad.qube_c6fee4a780 import IPythonKernel
from project.sparta_ab7a1c0e2d.sparta_a0284b3272.qube_72b49cf6cc import ReceiverKernel
def sparta_d1c969b0ee(file_path,text):
	A=file_path
	try:
		B='a'if os.path.exists(A)and os.path.getsize(A)>0 else'w'
		with open(A,B,encoding='utf-8')as C:
			if B=='a':C.write('\n')
			C.write(text)
		print(f"Successfully wrote/appended to {A}")
	except Exception as D:print(f"Error writing to file: {D}")
def sparta_312b20e849(api_key,worker_port,venv_str):
	C=venv_str;B=worker_port;print(f"BINDING ZMQ PORT NOW > {B}");E=zmq.Context();A=E.socket(zmq.ROUTER);A.bind(f"tcp://127.0.0.1:{B}");F=IPythonKernel(api_key);D=ReceiverKernel(F,A)
	if C!='-1':D.activate_venv(C)
	while True:G,H=A.recv_multipart();I=json.loads(H);D.process_request(G,I)
if __name__=='__main__':api_key=sys.argv[1];worker_port=sys.argv[2];venv_str=sys.argv[3];sparta_312b20e849(api_key,worker_port,venv_str)