import curses
from listview import ListView
from gameview import GameView
from controller import Controller
from utils import parse_json

JSON_FILE1 = "json/gameview.json"
def main(stdscr):
	"""
	A method for testing the view
	"""
	# Required:
	controller = Controller(stdscr)
	# Arbitrary data:
	view_name = "gameview"
	view_atr = parse_json(JSON_FILE1)
	# To draw views:
	controller.create_view(view_name, view_atr, GameView)
	# Program ends upon returning 0:
	return controller.begin()

if __name__ == "__main__":
	curses.wrapper(main)
