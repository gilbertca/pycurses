import json
import logging

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
		logging.debug(f"Function: * {function.__name__} * from: * {function.__globals__.get('__file__')} *")
		function(*args, **kwargs)
	
	return log

