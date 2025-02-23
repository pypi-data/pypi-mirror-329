import ast
def sparta_6278331c5e(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_3ffdfc1673(script_text):return sparta_6278331c5e(script_text)