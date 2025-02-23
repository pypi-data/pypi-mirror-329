_C='Windows'
_B='virtual_env_path'
_A='is_virtual_env'
import os,sys,platform,subprocess
if platform.system()==_C:import pythoncom,win32com.client
from pathlib import Path
from project.sparta_ab7a1c0e2d.sparta_8e998bb426 import qube_6d2235284c as qube_6d2235284c
from spartaqube_app.path_mapper_obf import sparta_638705750a
def sparta_8318efc52a(path):A=Path(path).resolve();return str(A).replace('\\','\\\\')
def sparta_25d492a6cf():
	B='virtual_env_name';C=hasattr(sys,'real_prefix')or hasattr(sys,'base_prefix')and sys.base_prefix!=sys.prefix
	if C:A=sys.prefix;D=os.path.basename(A);return{_A:True,B:D,_B:sparta_8318efc52a(A)}
	else:return{_A:False,B:None,_B:None}
def sparta_4ded3e7dad(bat_file_path,shortcut_path,icon_path):
	C=icon_path;B=shortcut_path;A=bat_file_path;pythoncom.CoInitialize()
	try:A=os.path.abspath(A);B=os.path.abspath(B);C=os.path.abspath(C);E=win32com.client.Dispatch('WScript.Shell');D=E.CreateShortcut(B);D.TargetPath=A;D.WorkingDirectory=os.path.dirname(A);D.IconLocation=C;D.Save();print('icon_path');print(C);print(f"Shortcut created at: {B}")
	finally:pythoncom.CoUninitialize()
def sparta_e77825a84d(shell_script_path,shortcut_name,icon_path):
	D=shell_script_path;B=shortcut_name;A=icon_path;D=os.path.abspath(D);A=os.path.abspath(A);C=f"/Applications/{B}.app";os.makedirs(f"{C}/Contents/MacOS",exist_ok=True);os.makedirs(f"{C}/Contents/Resources",exist_ok=True);E=f"{C}/Contents/MacOS/{B}"
	with open(E,'w')as F:F.write(f'#!/bin/bash\nosascript -e \'tell application "Terminal"\n    do script "bash {D}"\nend tell\'\n')
	os.chmod(E,493);G=f'''
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>CFBundleExecutable</key>
        <string>{B}</string>
        <key>CFBundleIconFile</key>
        <string>{os.path.basename(A)}</string>
        <key>CFBundleName</key>
        <string>{B}</string>
        <key>CFBundleIdentifier</key>
        <string>com.example.{B.lower()}</string>
        <key>CFBundleVersion</key>
        <string>1.0</string>
        <key>CFBundlePackageType</key>
        <string>APPL</string>
    </dict>
    </plist>
    ''';H=f"{C}/Contents/Info.plist"
	with open(H,'w')as I:I.write(G.strip())
	J=f"{C}/Contents/Resources/{os.path.basename(A)}"
	if os.path.exists(A):subprocess.run(['cp',A,J])
	else:print(f"Icon file not found: {A}")
	subprocess.run(['killall','Dock']);print(f"Shortcut created at: {C}");print(f"Logs will be written to /tmp/{B.lower()}_log.txt")
def sparta_daa63a5fe0(shortcut_name,shell_script_path,icon_path):
	C=icon_path;B=shell_script_path;A=shortcut_name;B=os.path.abspath(B);C=os.path.abspath(C);D=os.path.expanduser(f"~/Desktop/{A}.desktop");E=f'''[Desktop Entry]
Type=Application
Name={A}
Exec=gnome-terminal -- bash -c "bash {B}; exec bash"
Icon={C}
Terminal=true
'''
	with open(D,'w')as F:F.write(E)
	os.chmod(D,493);print(f"Launcher created at: {D}");print(f"Double-click the icon on your desktop to launch {A}.")
def sparta_9bede566bf(json_data,user_obj):
	S='SpartaQube Launcher';R='SpartaQube.sh';Q='SpartaQube.lnk';L='errorMsg';F='res';M=qube_6d2235284c.sparta_6aa5b44552(json_data,user_obj)
	if M[F]==1:
		T=M['token'];B=sparta_638705750a()['api'];A=sparta_8318efc52a(os.path.join(B,'spartaqube_exec.py'))
		if os.path.exists(A):
			try:os.remove(A)
			except Exception as D:return{F:-1,L:str(D)}
		U=f"""
from spartaqube import Spartaqube as Spartaqube

if __name__ == '__main__':
    Spartaqube(api_key='{T}', b_open_browser=True)

"""
		with open(A,'w')as H:H.write(U)
		G=sparta_8318efc52a(os.path.join(B,'spartaqube_launcher.py'))
		if os.path.exists(G):
			try:os.remove(G)
			except Exception as D:return{F:-1,L:str(D)}
		I=sparta_25d492a6cf();print('env_info');print(I)
		if I[_A]:E=I[_B];V=sparta_8318efc52a(os.path.join(f"{E}",'bin','python')if os.name!='nt'else os.path.join(f"{E}",'Scripts','python.exe'));N=sparta_8318efc52a(os.path.join(f"{E}",'bin/activate')if os.name!='nt'else os.path.join(E,'Scripts/activate.bat'));O=f'''
import os
import sys
import subprocess
import platform

def main_launcher():
    is_windows = platform.system() == "Windows"
    if not os.path.exists(\'{E}\'):
        print(f"Virtual environment not found")
        sys.exit(1)

    if not os.path.exists(\'{V}\'):
        raise FileNotFoundError(f"Python executable not found")
    if not os.path.exists(\'{A}\'):
        raise FileNotFoundError(f"Script not found")

    if is_windows:
        # On Windows: Activate the virtual environment using cmd.exe
        command = f\'cmd.exe /k "{N} && python "{A}"\'
        subprocess.run(command, shell=True)
    else:
        # On macOS/Linux: Use bash to activate the virtual environment
        command = f\'source "{N}" && python "{A}"\'
        subprocess.run(command, shell=True, executable="/bin/bash")

if __name__ == "__main__":
    main_launcher()
'''
		else:O=f'''
import os
import sys
import subprocess

def main_launcher():
    # Path to the Python executable in the file system
    python_executable = sys.executable

    if not os.path.exists(python_executable):
        print(f"Python executable not found in virtual environment")
        sys.exit(1)

    # Path to your application
    script_path = "{A}"

    if not os.path.exists(script_path):
        print(f"Application script not found: {A}")
        sys.exit(1)

    # Run the Python application
    subprocess.run([python_executable, script_path])

if __name__ == "__main__":
    main_launcher()
'''
		print('spartaqube_launcher');print(G)
		with open(G,'w')as H:H.write(O)
		W=sparta_638705750a()['spartaqube_path'];J=sparta_8318efc52a(os.path.join(W,'static','assets','images','Icon','favicon512.ico'));P=platform.system()
		if P==_C:
			C=sparta_8318efc52a(os.path.join(B,'SpartaQube.bat'));K=sparta_8318efc52a(os.path.join(B,Q))
			if os.path.exists(K):
				try:os.remove(K)
				except Exception as D:return{F:-1,L:str(D)}
			sparta_4ded3e7dad(C,K,J);X=os.path.join(os.path.expanduser('~'),'Desktop');Y=os.path.join(X,Q);sparta_4ded3e7dad(C,Y,J)
		elif P=='Darwin':C=sparta_8318efc52a(os.path.join(B,R));sparta_e77825a84d(shell_script_path=C,shortcut_name=S,icon_path=J)
		else:C=sparta_8318efc52a(os.path.join(B,R));sparta_daa63a5fe0(shell_script_path=C,shortcut_name=S,icon_path='/path/to/your/icon.png')
	return{F:1}