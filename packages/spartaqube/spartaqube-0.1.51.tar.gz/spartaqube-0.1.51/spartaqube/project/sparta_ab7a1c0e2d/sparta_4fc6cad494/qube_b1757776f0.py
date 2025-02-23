_E='Darwin'
_D='Windows'
_C=True
_B='errorMsg'
_A='res'
import os,subprocess,platform
from project.sparta_ab7a1c0e2d.sparta_4fc6cad494.qube_01c35b57ea import sparta_8318efc52a,sparta_f4bb722ba1
def sparta_fcaad28691(folder_path):
	A=folder_path;A=sparta_8318efc52a(A)
	if not os.path.isdir(A):return{_A:-1,_B:f"The folder path '{A}' does not exist."}
	C=platform.system()
	try:
		if C==_D:B=f'start cmd /c code "{A}"';os.system(B)
		elif C==_E:B=f'osascript -e \'tell application "Terminal" to do script "code \\"{A}\\" && exit"\'';subprocess.run(B,shell=_C)
		elif C=='Linux':B=f"gnome-terminal -- bash -c 'code \"{A}\"; exit'";subprocess.run(B,shell=_C)
		else:return{_A:-1,_B:f"Unsupported platform: {C}"}
	except Exception as D:return{_A:-1,_B:f"Failed to open folder in VSCode: {D}"}
	return{_A:1}
def sparta_ed9fcb26ed(folder_path):
	A=sparta_8318efc52a(folder_path)
	if not os.path.isdir(A):return{_A:-1,_B:f"The provided path '{A}' is not a valid directory."}
	B=platform.system()
	try:
		if B==_D:os.system(f'start cmd /K "cd /d {A}"')
		elif B=='Linux':subprocess.run(['x-terminal-emulator','--working-directory',A],check=_C)
		elif B==_E:C=f'''
            tell application "Terminal"
                do script "cd {A}"
                activate
            end tell
            ''';subprocess.run(['osascript','-e',C],check=_C)
		else:return{_A:-1,_B:'Unsupported operating system.'}
	except Exception as D:return{_A:-1,_B:f"Failed to open terminal at '{A}': {D}"}
	return{_A:1}