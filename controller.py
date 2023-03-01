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
		self.FUNCTIONS_DICT = {
			'x' : 0,
			'\t' : self.next_view,
		}
		self.function = lambda key_integer : self.FUNCTIONS_DICT.get(chr(key_integer))
		self.current_view_index = 0
		self.current_view_name = "" # The name the controller runs interact() on
		self.DEFAULT_TEXT = atr.get('default_text') if atr.get('default_text') is not None else curses.COLOR_WHITE
		self.DEFAULT_BACK = atr.get('default_back') if atr.get('default_back') is not None else curses.COLOR_BLACK
		self.colors = {} # A dictionary containing nested dict objects assigning colors.
		self.views_dict = {}
		self.views = self.views_dict.get

	@log
	def begin(self):
		"""
		Primary loop of any *pycurses program.
		Running this function passes control to the Controller,
			and key presses' functions are View specific.
		Will draw every view in it's own views_dict, and return 0
			upon program completion.
		"""
		# Sets focus to the 'first'
		first_view_name = list(self.views_dict)[self.current_view_index]
		for view_name in self.views_dict:
			self.draw_view(view_name)
		self.set_focus(view_name)
		return self.interact(first_view_name)

	@log
	def interact(self, view_name):
		"""
		Calls the selected view's interact function, and responds to the return code.
		"""
		while True:
			function = None # Required for references to function
			response = self.views(self.current_view_name).interact()
			# Conditional required for 'non-responsive' view functions.
			if response is not None:
				function = self.function(response)
			# Conditional to exit program:
			if function == 0:
				return 0
			# Conditional if keypress results in a function:
			elif function is not None:
				function()

	@log
	def set_focus(self, view_name):
		"""
		Sets self.current_view_name to the passed view name.
		"""
		self.current_view_name = view_name

	@log
	def next_view(self):
		"""
		Runs self.focus on the next view in the list.
		"""
		if self.current_view_index == len(self.views_dict) - 1:
			self.current_view_index = 0
		else:
			self.current_view_index += 1
		# Get the next view name:
		next_view_name = list(self.views_dict)[self.current_view_index]
		# Set focus to the next view:
		self.set_focus(next_view_name)

	@log
	def create_view(self, view_name, view_atr, ViewClass):
		"""
		Takes a string name, a dictionary of attributes, 
			and a Class reference to initialize the view as.
		"""
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
		if self.colors.get(view).get("background_color") is None:
			self.colors.get(view).update({"background_color" : 0}) # 0 is curses default for W/B

	@log
	def _next_color_pair(self):
		"""
		Returns an integer corresponding to the free integer for curses color pairs
		"""
		count = 0
		for view_name in self.views_dict:
			# These three lines could be one, but are three for simplicity's sake.
			view = self.views(view_name)
			color_dict = self.colors.get(view)
			count += len(color_dict)
		return count + 1
