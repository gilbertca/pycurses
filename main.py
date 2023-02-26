import curses
from listview import ListView
from controller import Controller
from utils import parse_json

JSON_FILE1 = "json/listview1.json"
JSON_FILE2 = "json/listview2.json"
def main(stdscr):
	"""
	A method for testing the view
	"""
	# Required:
	controller = Controller(stdscr)
	# Arbitrary data:
	view_name = "listview"
	view_name2 = "listview2"
	view_atr = parse_json(JSON_FILE1)
	view_atr2 = parse_json(JSON_FILE2)
	# To draw views:
	controller.create_view(view_name, view_atr, ListView)
	controller.create_view(view_name2, view_atr2, ListView)
	# Program ends upon returning 0:
	return controller.begin()

if __name__ == "__main__":
	curses.wrapper(main)
