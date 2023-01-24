import json

def parse_json(file_name):
	"""Simple utility to read from a JSON file"""
	json_file = open(file_name)
	data = json.load(json_file)
	json_file.close()
	return data
