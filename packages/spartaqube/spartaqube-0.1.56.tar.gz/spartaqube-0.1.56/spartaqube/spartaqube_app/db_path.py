_A='windows'
import os,sys,getpass,platform
def sparta_b4c3d14efc(full_path,b_print=False):
	B=b_print;A=full_path
	try:
		if not os.path.exists(A):
			os.makedirs(A)
			if B:print(f"Folder created successfully at {A}")
		elif B:print(f"Folder already exists at {A}")
	except Exception as C:print(f"An error occurred: {C}")
def sparta_a93cc5ef0f():
	A=platform.system()
	if A=='Windows':return _A
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
def sparta_5f28d88604():
	D=os.getenv('IS_REMOTE_SPARTAQUBE_CONTAINER','False')
	if D=='True':C='/app/APPDATA/local_db/db.sqlite3'
	else:
		B=sparta_a93cc5ef0f()
		if B==_A:A=f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\SpartaQube\\data"
		elif B=='linux':A=os.path.expanduser('~/SpartaQube/data')
		elif B=='mac':A=os.path.expanduser('~/Library/Application Support\\SpartaQube\\data')
		sparta_b4c3d14efc(A);C=os.path.join(A,'db.sqlite3')
	return C