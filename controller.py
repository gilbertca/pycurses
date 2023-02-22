import curses
import logging
from listview import ListView
from baseview import AbstractBaseView
from utils import log

class Controller:
	"""
	Controller needs to map colors in order to keep track of arbitrary number of color pairs.
	Controller needs to call draw methods for view objects
	"""
	def __init__(self, stdscr, views_dict=None, **atr):
		logging.basicConfig(filename='pycurses.log', filemode='w', level=logging.DEBUG)
		self.stdscr = stdscr
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
		self.DEFAULT_TEXT = atr.get('default_text') if atr.get('default_text') is not None else curses.COLOR_WHITE
		self.DEFAULT_BACK = atr.get('default_back') if atr.get('default_back') is not None else curses.COLOR_BLACK
		"""
			self.colors should look like this:
			self.colors = {
				view : {
					"*_color" : pair_num,
				},
			}
		"""
		self.colors = {}
		self.views_dict = {}
		self.views = self.views_dict.get

	@log
	def create_view(self, view_name, view_atr, ViewClass):
		"""Takes a string name, a dictionary of attributes, and a Class reference to instantiate the view as."""
		view = ViewClass(self, **view_atr)
		self.views_dict.update({view_name : view})
		self.map_colors(view)

	@log
	def draw_view(self, view_name):
		self.views(view_name).create_window()
		self.views(view_name).draw_window()

	@log
	def get_view(self, view_name):
		return self.views(view_name)

	@log
	def get_color(self, view, color_name):
		return self.colors.get(view).get(color_name)

	@log
	def map_colors(self, view):
		"""
		Links colors to color pair integers
		NEED TO ADD DEFAULTS FOR TEXT_COLOR AND BACKGROUND_COLOR SHOULD THEY NOT BE PROVIDED IN THE JSON FILE
		"""
		self.colors.update({view : {}})
		for atr in view.atr_dict: # Loop through the attributes of each view
			if "color" in atr: # Any attribute containing "color" in the key will be checked here
				pair_num = self._next_color_pair()
				color_value = view.atr(atr) # Get color list/string from view.atr
				# Length of colors + 1 always equals the next curses color pair to initialize
				if isinstance(color_value, list): # If list -> Assign [0] as fore and [1] as back
					colors = [self.CURSES_COLOR_MAP.get(color) for color in color_value]
					self.colors.get(view).update({atr : pair_num})
					curses.init_pair(pair_num, *colors)
				elif isinstance(color_value, str): # If string -> Assign string as fore and back as view.DEFAULT_BACK
					color = self.CURSES_COLOR_MAP.get(color_value)
					self.colors.get(view).update({atr : pair_num})
					curses.init_pair(pair_num, color, self.DEFAULT_BACK)
		# This line may need to be removed? Not sure if this functionality is intended
		if self.colors.get(view).get("text_color") is None: # Default if there are no colors passed
			self.colors.get(view).update({"text_color" : 0}) # 0 is curses default for W/B

	@log
	def _next_color_pair(self):
		"""
		Returns an integer corresponding to the free integer for curses color pairs
		"""
		count = 0
		for view_name in self.views_dict:
			view = self.views(view_name)
			color_dict = self.colors.get(view)
			count += len(color_dict)
		return count + 1
