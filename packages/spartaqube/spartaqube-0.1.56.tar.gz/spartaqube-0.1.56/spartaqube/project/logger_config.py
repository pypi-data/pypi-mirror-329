from loguru import logger
import os,sys
logger.remove()
LOG_FORMAT='<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <cyan>{level}</cyan> |\n<white>{message}</white>\n'
logger.add(sys.stdout,format=LOG_FORMAT,level='DEBUG')