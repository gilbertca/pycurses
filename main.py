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
	# TODO: Condense these 2 calls into 1 shortcut call
	controller.create_view(view_name, view_atr, ListView)
	controller.create_view(view_name2, view_atr2, ListView)
	return controller.begin()
	#controller.draw_view("listview")
	#controller.draw_view("listview2")
	# This line is to pause before ending. From here,
	#	control should be handed off and allow interactibility
	#key_pressed = controller.get_view("listview").screen.getch()
	#if key_pressed == ord("x"):
	#	curses.napms(1000)
	# Returning *anything* ends a curses session.
	#	Perhaps this should be return Controller.run()
	#	or something along those lines.

if __name__ == "__main__":
	curses.wrapper(main)
