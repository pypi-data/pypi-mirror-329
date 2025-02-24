import ast
def sparta_8bc4c8f517(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_aa3be78779(script_text):return sparta_8bc4c8f517(script_text)