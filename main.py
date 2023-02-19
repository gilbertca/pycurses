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
	controller = Controller()
	# Arbitrary data:
	view_name = "listview"
	view_atr = parse_json(JSON_FILE1)
	# To draw views:
	controller.create_view(view_name, view_atr, ListView)
	controller.draw_view("listview")
	controller.get_view("listview").screen.getch()
	return 0

if __name__ == "__main__":
	curses.wrapper(main)
