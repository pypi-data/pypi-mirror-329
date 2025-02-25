import ast
def sparta_23f80c47ec(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_738e46c3f0(script_text):return sparta_23f80c47ec(script_text)