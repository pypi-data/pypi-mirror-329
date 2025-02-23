import time
def sparta_eca0bc859b():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_eca0bc859b()
def sparta_37d4291f6d(tempBool=True):
	A=next(TicToc)
	if tempBool:print('Elapsed time: %f seconds.\n'%A);return A
def sparta_262367e232():sparta_37d4291f6d(False)