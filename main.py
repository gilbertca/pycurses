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
	# TODO: Condense these 2 calls into 1 shortcut call
	controller.create_view(view_name, view_atr, ListView)
	controller.draw_view("listview")
	# This line is to pause before ending. From here,
	#	control should be handed off and allow interactibility
	controller.get_view("listview").screen.getch()
	# Returning *anything* ends a curses session.
	return 0

if __name__ == "__main__":
	curses.wrapper(main)
