_A='windows'
import os,sys,getpass,platform
def sparta_c6d3a8a8be(full_path,b_print=False):
	B=b_print;A=full_path
	try:
		if not os.path.exists(A):
			os.makedirs(A)
			if B:print(f"Folder created successfully at {A}")
		elif B:print(f"Folder already exists at {A}")
	except Exception as C:print(f"An error occurred: {C}")
def sparta_40fbb95963():
	A=platform.system()
	if A=='Windows':return _A
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
def sparta_663b5cbb00():
	D=os.getenv('IS_REMOTE_SPARTAQUBE_CONTAINER','False')
	if D=='True':C='/app/APPDATA/local_db/db.sqlite3'
	else:
		B=sparta_40fbb95963()
		if B==_A:A=f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\SpartaQube\\data"
		elif B=='linux':A=os.path.expanduser('~/SpartaQube/data')
		elif B=='mac':A=os.path.expanduser('~/Library/Application Support\\SpartaQube\\data')
		sparta_c6d3a8a8be(A);C=os.path.join(A,'db.sqlite3')
	return C