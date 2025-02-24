import time
from project.logger_config import logger
def sparta_4be6d87d73():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_4be6d87d73()
def sparta_039b88f342(tempBool=True):
	A=next(TicToc)
	if tempBool:logger.debug('Elapsed time: %f seconds.\n'%A);return A
def sparta_be6a742061():sparta_039b88f342(False)