import json
import logging
from datetime import datetime

def parse_json(file_name):
	"""Simple utility to read from a JSON file returns a dict object"""
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

def errorh(function):
	"""Decorator to wrap functions with try/except blocks."""
	def errorh(*args, **kwargs):
		try:
			function()
		except:
			logging.critical(f"*Critical error* * {datetime.now()} * with * {function.__name__} * due to")
			raise

	return errorh
