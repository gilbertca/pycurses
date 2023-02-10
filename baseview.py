import curses
import math
import logging
from utils import parse_json, log


class AbstractBaseView:
	"""
	An abstraction from which all views will inherit.
	Contains methods which must be overloaded by its children
	"""
	def __init__(self, FILE, **atr):
		logging.basicConfig(filename='pycurses.log', filemode='w', level=logging.DEBUG)
		# Constant values:
		self.atr_dict = FILE # Contains all attributes
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

	@log
	def create_window(self):
		"""Creates a pad or window object based on given parameters"""
		self._calculate_size()
		self._calculate_window_valign()
		self._calculate_window_halign()
		self._map_colors() # init color pairs for use using provided string keywords
		self.screen = curses.newpad(self.height, self.width)
	
	@log
	def draw_window(self):
		"""
		To be overloaded by child.
		"""
		raise Exception(f"This method must be overloaded by it's child.")

	@log
	def determine_color(self, string):
		"""
		To be overloaded by child.
		"""
		raise Exception(f"This method must be overloaded by it's child.")

	@log
	def _calculate_size(self):
		"""Method run by create_window to calculate height and width"""
		# Height calculations:
		height = self.atr('height')
		vborder = self.atr('vborder')
		vpercent = self.atr('vpercent')
		if height: # If given height:
			self.height = height
		elif vborder: # If given vborder:
			self.height = curses.LINES - (2 * vborder)
		elif vpercent:
			self.height = math.floor(curses.LINES * vpercent / 100)
		else: # Default: full height
			self.height = curses.LINES
		# Width calculations:
		width = self.atr('width')
		hborder = self.atr('hborder')
		hpercent = self.atr('hpercent')
		if width: # No border / No height case
			self.width = width
		elif hborder: # Border only case
			self.width = curses.COLS - (2 * hborder)
		elif hpercent: # Height only case
			self.width = math.floor(curses.COLS * hpercent / 100)
		else: # Default to full width 
			self.width = curses.COLS

	@log
	def _calculate_window_valign(self):
		"""Method run by create_window() to calculate topy and boty for draw_window()"""
		# Note: assignment of -1 is to prevent type errors when comparing int to nonetype
		topy = self.atr('topy')
		boty = self.atr('boty')
		valign = self.atr('valign')
		if topy and boty:
			self.topy = topy
			self.boty = boty
		if valign == 'center' or valign == None: # Center is default alignment
			center = math.floor(curses.LINES/2) # Always move up 1 from center if odd!
			self.topy = center - math.floor(self.height/2) # Always move up 1!
			self.boty = center + math.ceil(self.height/2) # Always move up 1!
		if valign == 'top':
			self.topy = 0
			self.boty = 0 + self.height - 1
		if valign == 'bottom':
			self.topy = curses.LINES - 1
			self.boty = curses.LINES - self.height

	@log
	def _calculate_window_halign(self):
		"""Method run by create_window() to calculate topx and botx for draw_window()"""
		leftx = self.atr('leftx')
		rightx = self.atr('rightx')
		halign = self.atr('halign')
		if leftx and rightx:
			self.leftx = leftx
			self.rightx = rightx
		if halign == 'center' or halign == None:
			center = math.floor(curses.COLS/2) # Always move left 1 from center if odd!
			self.leftx = center - math.floor(self.width/2) # Alwas move left 1!
			self.rightx = center + math.ceil(self.width/2) # Always move left 1!
		if halign == 'left':
			self.leftx = 0
			self.rightx = 0 + self.width - 1
		if halign == 'right':
			self.leftx = curses.COLS - self.width
			self.rightx = curses.COLS - 1

	@log
	def _get_padding(self):
		padding = self.atr('padding') if self.atr('padding') else 0
		hpadding = self.atr('hpadding') if self.atr('hpadding') else 0
		vpadding = self.atr('vpadding') if self.atr('vpadding') else 0
		if padding:
			vpadding = hpadding = padding
		return vpadding,hpadding

	@log
	def _map_colors(self):
		"""
		Links colors to color pair integers
		"""
		for atr in self.atr_dict: # Loop through self.atr
			if "color" in atr: # Color only contained by values which set colors
				color_value = self.atr(atr) # Get color list/string from self.atr
				pair_num = self.COLOR_PAIR_MAP.get(atr) # COLOR_MAP links the color key to a pair number for curses
				if isinstance(color_value, list): # If list -> Assign [0] as fore and [1] as back
					# Need to relate list values to CURSES_COLOR_MAP
					colors = [self.CURSES_COLOR_MAP.get(color) for color in color_value]
					curses.init_pair(pair_num, *colors)
				elif isinstance(color_value, str): # If string -> Assign string as fore and back as self.DEFAULT_BACK
					# Need to relate string value to CURSES_COLOR_MAP
					color = self.CURSES_COLOR_MAP.get(color_value)
					curses.init_pair(pair_num, color, self.DEFAULT_BACK)
				elif color_value is None: # If None -> Default white on black
					curses.init_pair(pair_num, self.DEFAULT_TEXT, self.DEFAULT_BACK)
