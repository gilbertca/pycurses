import json
import logging
from datetime import datetime

def parse_json(file_name):
	"""Simple utility to read from a JSON file"""
	json_file = open(file_name)
	data = json.load(json_file)
	json_file.close()
	return data

def log(function):
	"""Decorator to log info about internal functions"""
	def log(*args, **kwargs):
		# String extractions done here:
		logging.debug(f"{datetime.now()} Function: * {function.__name__} * from: * {function.__globals__.get('__file__')} *")
		logging.info(f"{datetime.now()} Attempting {function.__name__}.")
		function(*args, **kwargs)
	
	return log
