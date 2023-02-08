import curses
import math
import logging
from utils import parse_json, log

JSON_FILE_TEXT = "TEXT.json"
JSON_FILE_WINDOW = "json/listview.json"

class AbstractBaseView:
	"""
	An abstraction from which all views will inherit.
	Contains methods which must be overloaded by its children
	"""
	def __init__(self, **atr):
		logging.basicConfig(filename='pycurses.log', filemode='w', level=logging.DEBUG)
		# Constant values:
		self.TEXT = parse_json(JSON_FILE_TEXT).get # Similar to atr, saving typing .get()
		self.atr_dict = parse_json(JSON_FILE_WINDOW)
		self.atr = self.atr_dict.get # use self.atr('key') saving typing .get()
		self.BACKGROUND_FILL = self.atr('background_fill') if self.atr('background_fill') is not None else ' '
		self.DEFAULT_TEXT = curses.COLOR_BLACK
		self.DEFAULT_BACK = curses.COLOR_WHITE
		self.COLOR_PAIR_MAP = {
			'text_color' : 1,
			'background_color' : 2,
			'important_color' : 3,
		}
		self.CURSES_COLOR_MAP = {
			'black' : curses.COLOR_BLACK,
			'red' : curses.COLOR_RED,
			'green' : curses.COLOR_GREEN,
			'yellow' : curses.COLOR_YELLOW,
			'blue' : curses.COLOR_BLUE,
			'magenta' : curses.COLOR_MAGENTA,
			'cyan' : curses.COLOR_CYAN,
			'white' : curses.COLOR_WHITE,
		}
		# self.color -> saves repeated typing of curses.color_pair(CURSES_...
		self.color = lambda type : curses.color_pair(self.COLOR_PAIR_MAP.get(type))
		# Temporary value to be replaced with a class specific method:
		#	ListView will iterate through a given list, for example.
		self.iterable = [n for n in self.atr_dict]
		# Steps to create window:
		# Note: all initializations must come before this point
		self.create_window() # create a pad of fixed dimensions based on string keywords
		self.draw_window() # draw text to screen
