import curses
from listview import ListView
from gameview import GameView, InventoryView
from controller import Controller
from utils import parse_json

JSON_FILE1 = "json/gameview.json"
JSON_FILE2 = "json/listview.json"
def main(stdscr):
	"""
	A method for testing the view
	"""
	# Required:
	controller = Controller(stdscr)
	# Arbitrary data:
	view_name = "gameview"
	view_n2 = "listview"
	view_atr = parse_json(JSON_FILE1)
	view_a2 = parse_json(JSON_FILE2)
	# To draw views:
	controller.create_view(view_name, view_atr, GameView)
	controller.create_view(view_n2, view_a2, InventoryView)
	# Program ends upon returning 0:
	return controller.begin()

if __name__ == "__main__":
	curses.wrapper(main)
