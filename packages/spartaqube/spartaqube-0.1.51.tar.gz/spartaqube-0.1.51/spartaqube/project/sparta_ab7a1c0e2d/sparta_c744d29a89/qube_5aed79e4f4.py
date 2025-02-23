_L='is_git_repository'
_K='You need to create a notebook first (you can save this notebook with CTRL+ALT+S first)'
_J='url'
_I='name'
_H='scm'
_G='An unexpected error occurred, please try again'
_F=None
_E=False
_D='errorMsg'
_C='projectPath'
_B=True
_A='res'
import os,re,time,json,shutil,git
from asyncio import subprocess
from re import S
from dateutil import parser
from subprocess import Popen,PIPE
from django.contrib.humanize.templatetags.humanize import naturalday
def sparta_eb3fa0aafb(path):
	try:A=git.Repo(path).git_dir;return _B
	except git.exc.InvalidGitRepositoryError:return _E
def sparta_d182f1723d(json_data,user_obj):
	A=json_data['notebookProjectId'];B,C=qube_1fe7fcee70.get_notebookProjectObj(A,user_obj)
	if B is not _F:return _B
	return _E
def sparta_788b160bac(remoteBranchToTrack):A=Popen(f"git branch -u {remoteBranchToTrack}",stdout=PIPE,stderr=subprocess.STDOUT,bufsize=1,universal_newlines=_B,shell=_B);B=A.stdout.readline();print('realtime_output 1');print(B);A=Popen(f"git config push.default upstream",stdout=PIPE,stderr=subprocess.STDOUT,bufsize=1,universal_newlines=_B,shell=_B);print('realtime_output 2');print(B)
def sparta_66d8429471(func):
	def A(json_data,user_obj):
		B=user_obj;A=json_data
		if not sparta_d182f1723d(A,B):return{_A:-1,_D:_K}
		return func(A,B)
	return A
def sparta_0b1003aab8(func):
	def A(webSocket,json_data,user_obj):
		B=user_obj;A=json_data
		if not sparta_d182f1723d(A,B):return{_A:-1,_D:_K}
		return func(webSocket,A,B)
	return A
def sparta_162c8a4ddb(repo,user_obj):
	C='user';A=user_obj;D=A.email;E=f"{A.first_name.capitalize()} {A.last_name.capitalize()}"
	with repo.config_writer()as B:B.set_value(C,_I,E);B.set_value(C,'email',D)
def sparta_de73672893(webSocket,json_data,user_obj):
	A=json_data;print('sqEditorGitClone');print(A);F=A[_C];G=A['bCreateRepoAtPath'];K=A['folder_name'];H=A['file_path'];I=A['cloneUrl'];C=F
	if G:C=H
	J=os.path.dirname(os.path.realpath(__file__));os.chdir(C);D=Popen(f"git clone {I} --progress",stdout=PIPE,stderr=subprocess.STDOUT,bufsize=1,universal_newlines=_B,shell=_B);os.chdir(J);E=_E
	while _B:
		B=D.stdout.readline()
		if'Receiving objects:'in B:E=_B,
		if B==''and D.poll()is not _F:break
		if B:webSocket.send(text_data=json.dumps({_A:2,'msg':B}))
	if E:return{_A:1}
	else:return{_A:-1,_D:'An error occurred'}
def sparta_a10c85b7a9(json_data,user_obj):
	A=json_data;B=A[_C];I=A.get('bAddGitignore',_E);J=A.get('bAddReadme',_E);C=Popen(f"git init",stdout=PIPE,stderr=subprocess.STDOUT,bufsize=1,universal_newlines=_B,shell=_B,cwd=B);F=[]
	for G in C.stdout:print('Git create repo txt');print(G,end='');F.append(G.strip())
	C.stdout.close();C.wait();H=os.path.dirname(__file__)
	if I:
		D=os.path.join(H,'.default_gitignore');E=os.path.join(B,'.gitignore')
		try:shutil.copy(D,E)
		except:pass
	if J:
		D=os.path.join(H,'.default_readme');E=os.path.join(B,'README.md')
		try:shutil.copy(D,E)
		except:pass
	return{_A:1,'output':'\n'.join(F)}
def sparta_834c8ffc12(json_data,user_obj):
	F=user_obj;B=json_data;print('sqEditorGitAddRemoteOrigin json_data');print(B);C=B[_C];G=sparta_eb3fa0aafb(C)
	if G:
		H=B['remoteUrl'];I=B['remoteName'];A=git.Repo(C);sparta_162c8a4ddb(A,F);J=A.create_remote(I,url=H);A=git.Repo(C);sparta_162c8a4ddb(A,F)
		for D in A.remotes:D.fetch()
		for D in A.remotes:
			if J==D:
				E=D.refs
				if len(E)>0:K=E[len(E)-1];L=os.path.dirname(os.path.realpath(__file__));os.chdir(C);sparta_788b160bac(K);os.chdir(L)
	return{_A:1}
def sparta_0696faec7a(json_data,user_obj):
	A=json_data;print('git_load_available_track_remote json_data');print(A);B=A[_C];F=sparta_eb3fa0aafb(B)
	if F:
		G=A[_H];C=git.Repo(B);sparta_162c8a4ddb(C,user_obj);D=[]
		for E in C.remotes:
			if G==E.config_reader.get(_J):
				for H in E.refs:D.append({_I:H.name})
	return{_A:1,'available_branches':D}
def sparta_a80890892d(json_data,user_obj):
	A=json_data;print('*******************************************');print('git_set_track_remote json_data');print(A);B=A[_C];D=sparta_eb3fa0aafb(B)
	if D:G=A[_H];E=A['remoteBranchToTrack'];C=git.Repo(B);sparta_162c8a4ddb(C,user_obj);H=C.head.ref.name;F=os.path.dirname(os.path.realpath(__file__));os.chdir(B);sparta_788b160bac(E);os.chdir(F)
	return{_A:1}
@sparta_66d8429471
def sparta_622aa5db93(json_data,user_obj):return{_A:1}
def sparta_c28186758f(json_data,user_obj):
	B=json_data[_C];C=sparta_eb3fa0aafb(B)
	if C:A=git.Repo(B);sparta_162c8a4ddb(A,user_obj);D=A.active_branch;E=D.tracking_branch().remote_name;F=A.remote(name=E);F.pull(allow_unrelated_histories=_B)
	return{_A:1}
def sparta_b4a4cd8db4(json_data,user_obj):
	B=json_data[_C];C=sparta_eb3fa0aafb(B)
	if C:A=git.Repo(B);sparta_162c8a4ddb(A,user_obj);D=A.active_branch;E=D.tracking_branch().remote_name;F=A.remote(name=f"{E}");F.push()
	return{_A:1}
def sparta_bdb3ed3dba(json_data,user_obj):
	A=json_data[_C];C=sparta_eb3fa0aafb(A)
	if C:
		B=git.Repo(A);sparta_162c8a4ddb(B,user_obj)
		for D in B.remotes:D.fetch()
	return{_A:1}
def sparta_9ddb3399fd(json_data,user_obj):A=json_data[_C];B=sparta_eb3fa0aafb(A);return{_A:1,_L:B}
def sparta_1689220a68(json_data,user_obj):
	Y='time_sort';O='is_git_repo';G='sha'
	def N(commit):A=commit;B=time.strftime('%Y-%m-%d %H:%M',time.localtime(A.committed_date));C=naturalday(parser.parse(str(B)));return{'author':A.committer.name,'author_name':A.author.name,'time':C,Y:B,G:A.hexsha,'message':A.message,'summary':A.summary}
	def B(folder_path):
		j='remotes_arr';i='commits_ahead_arr';h='commits_behind_arr';g='is_ahead';f='is_behind';W='branch';H=folder_path;P=sparta_eb3fa0aafb(H);print(f"is_git_repository > {H}");print(P)
		if P:
			A=git.Repo(H);F=[];Z=[]
			for a in A.references:
				b=a.name;Z.append(b)
				for k in A.iter_commits(rev=b):B=N(k);B[W]=a.name;B[f]=0;B[g]=0;F.append(B)
			F=sorted(F,key=lambda d:d[Y],reverse=_B);I=A.head.ref.name;K=[];L=[]
			if len(A.remotes)>0:
				c=A.active_branch;Q=_F;D=c.tracking_branch()
				if D is not _F:
					M=c.tracking_branch().name;print(f"current_branch > {I}");print(f"remote_branch > {M}");print('branch.tracking_branch()');print(D);print(dir(D));print(D.path);print('Remote Name');print(D.remote_name);Q=D.remote_name;l=D.config_reader();print('remote_branch_url');print(l)
					try:
						m=A.iter_commits(f"{I}..{M}")
						for n in m:B=N(n);K.append(B)
						print(h);print(K)
					except Exception as R:print('Exception behind');print(R)
					try:
						o=A.iter_commits(f"{M}..{I}")
						for p in o:B=N(p);L.append(B)
						print(i);print(L)
					except Exception as R:print('Exception Ahead');print(R)
					for S in K:
						T=S[G]
						for E in F:
							if E[W]==f"{M}"and E[G]==T:E[f]=1;break
					for S in L:
						T=S[G]
						for E in F:
							if E[W]==I and E[G]==T:E[g]=1;break
			U=[]
			for J in A.remotes:
				d=_E;print('----------------------------');print('this_remote');print(J);print(dir(J))
				if Q is not _F:
					if Q==J.name:d=_B
				V=J.config_reader.get(_J);q=os.path.splitext(os.path.basename(V))[0];C=re.search('@[\\w.]+',V)
				if C is not _F:
					C=str(C.group())
					if C.startswith('@'):C=C[1:]
				else:C=''
				U.append({_I:J.name,_H:V,'repo_name':q,'domain':C,'is_tracking':d})
			print(j);print(U);e=_E
			if X==H:e=_B
			return{_A:1,'is_base_directory':e,'folder':H,O:P,'commits_arr':F,'branches':Z,'current_branch':I,j:U,h:K,i:L}
	X=json_data[_C];A=B(X)
	if A is not _F:A[O]=_B;return A
	else:return{_A:1,O:_E}
def sparta_8b05c5c41e(json_data,user_obj):
	H='path';G='file';C=json_data[_C];I=sparta_eb3fa0aafb(C)
	if I:
		B=git.Repo(C);sparta_162c8a4ddb(B,user_obj);D=[]
		for A in B.index.diff(_F):D.append({G:A.a_path,'change_type':A.change_type,'is_deleted':A.deleted_file,H:A.a_path})
		E=[]
		for F in B.untracked_files:E.append({G:F,H:F})
		return{_A:1,'changed_files_arr':D,'untracked_files_arr':E}
	return{_A:1}
def sparta_259266793d(json_data,user_obj):
	B=json_data;C=B[_C];D=B['gitMsg'];E=sparta_eb3fa0aafb(C)
	if E:A=git.Repo(C);sparta_162c8a4ddb(A,user_obj);A.git.add(all=_B);A.git.commit('-m',D)
	return{_A:1}
@sparta_66d8429471
def sparta_2a1370ec7e(json_data,user_obj):return{_A:1}
def sparta_1608ac4b72(json_data,user_obj):
	A=json_data;print('Delete Remoete');print(A);C=A[_C];E=sparta_eb3fa0aafb(C)
	if E:
		B=git.Repo(C);sparta_162c8a4ddb(B,user_obj);F=A[_H]
		for D in B.remotes:
			if F==D.config_reader.get(_J):B.delete_remote(D);break
	return{_A:1}
def sparta_f38f841d4c(json_data,user_obj):return{_A:1}
def sparta_f817d9df61(json_data,user_obj):
	D=json_data;E=D[_C];C=D['newBranchName'];F=sparta_eb3fa0aafb(E)
	if F:
		A=git.Repo(E);sparta_162c8a4ddb(A,user_obj);B=[A for A in A.branches if A.name==C]
		if len(B)==0:G=A.active_branch;B=A.create_head(C);B.checkout();A.git.push('--set-upstream','origin',B);G.checkout();A.git.checkout(C);return{_A:1}
		else:return{_A:-1,_D:'A branch with this name already exists'}
	return{_A:-1,_D:_G}
def sparta_1c6c91715e(json_data,user_obj):
	A=json_data;B=A[_C];D=A['branch2Checkout'];E=sparta_eb3fa0aafb(B)
	if E:
		C=git.Repo(B);sparta_162c8a4ddb(C,user_obj)
		try:C.git.checkout(D);return{_A:1}
		except Exception as F:return{_A:-1,_D:str(F)}
	return{_A:-1,_D:_G}
def sparta_b7f467f193(json_data,user_obj):
	B=json_data;C=B[_C];D=B['branch2Merge'];F=sparta_eb3fa0aafb(C)
	if F:
		A=git.Repo(C);sparta_162c8a4ddb(A,user_obj);E=A.head.ref.name
		if E==D:return{_A:-1,_D:'Please choose another branch'}
		try:A.git.checkout(D);A.git.merge(E);return{_A:1}
		except Exception as G:return{_A:-1,_D:str(G)}
	return{_A:-1,_D:_G}
def sparta_17aaf3b78a(json_data,user_obj):
	D=json_data;A=D[_C];B=D['branch2Delete'];F=sparta_eb3fa0aafb(A)
	if F:
		E=git.Repo(A);sparta_162c8a4ddb(E,user_obj);G=E.head.ref.name
		if G==B:return{_A:-1,_D:'You cannot delete the active branch. Please checkout to another branch before deleting this one'}
		try:H=os.path.dirname(os.path.realpath(__file__));os.chdir(A);C=Popen(f"git branch -d {B}",stdout=PIPE,stderr=PIPE,bufsize=1,universal_newlines=_B,shell=_B);I=C.stderr.readlines();C=Popen(f"git push origin --delete {B}",stdout=PIPE,stderr=PIPE,bufsize=1,universal_newlines=_B,shell=_B);I=C.stderr.readlines();os.chdir(H);return{_A:1}
		except Exception as J:return{_A:-1,_D:str(J)}
	return{_A:-1,_D:_G}
def sparta_02d5922950(json_data,user_obj):
	F='diff_output';A=json_data;print('sqEditorGitLoadFilesDiff');print(A);B=A[_C];G=A['filePath'];H=A['fileType'];C=sparta_eb3fa0aafb(B);print(_L);print(C)
	if C:D=git.Repo(B);sparta_162c8a4ddb(D,user_obj);E=D.git.diff();print(F);print(E);return{_A:1,F:E}
	return{_A:-1,_D:_G}