import time
from project.logger_config import logger
def sparta_2326a9934e():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_2326a9934e()
def sparta_def08f10b2(tempBool=True):
	A=next(TicToc)
	if tempBool:logger.debug('Elapsed time: %f seconds.\n'%A);return A
def sparta_9fbfc9b103():sparta_def08f10b2(False)