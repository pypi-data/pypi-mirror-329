def sparta_27d5b4da7a(s):
	if isinstance(s,str):
		s=s.strip().lower()
		if s in['true','1','yes','y']:return True
		elif s in['false','0','no','n']:return False
	raise ValueError(f"Cannot convert '{s}' to a boolean.")
def sparta_bef5214e22(assign_dict):
	A=assign_dict;C=A['guiType'];B=A['value']
	if C=='boolean':
		if not isinstance(B,bool):B=sparta_27d5b4da7a(B)
	D=f"import json\n{A['variableState']} = json.loads({A['interactiveVarDict']})";E=f"{A['variable']} = {B}";return{'assign_code':E,'assign_state_variable':D}