import curses
import math
import logging
from utils import parse_json, log

# Note: Reading all class attributes from json files, allowing interface to be created
# Via a collection of json files
# Logging setup:
# Json file location:
JSON_FILE_TEXT = "TEXT.json"
JSON_FILE_WINDOW = "json/listview.json"

class Focusable:
	"""An inheritable abtract class which allows a window object to take focus"""
	pass

class Scrollable:
	"""
	An inheritable abstract class which allows a window object to scroll
	Objects should override the .draw() method
	"""
	pass

class ListView:
	"""
	A class to display a curses list given a window/pad object, and a list
	Also accepts several key word parameters
	The object can be created as a list, or as a pad
	Like half, quarter, third, etc.
	Also top, bottom, left right, center
	Width can be a keyword string, or a numeric value
	"""
	# More to be added as more requirements are needed
	# Also need to be able to generate arbitrary color mappings
	# Need to define/declare variables regarding color pairs
	def __init__(self, **atr):
		logging.basicConfig(filename='pycurses.log', filemode='w', level=logging.DEBUG)
		# Constant values:
		self.COLOR_MAP = {
		'text' : 1,
		'background' : 2,
		'important' : 3,
		}
		self.DEFAULT_TEXT = curses.COLOR_BLACK
		self.DEFAULT_BACK = curses.COLOR_WHITE
		self.TEXT = parse_json(JSON_FILE_TEXT).get # Similar to atr, saving typing .get()
		self.atr_dict = parse_json(JSON_FILE_WINDOW)
		self.atr = self.atr_dict.get # use self.atr('key') saving typing .get()
		self.colors = {}
		# Temporary value:
		self.iterable = [n for n in self.atr_dict]
		# Steps to create window:
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
		"""Draw the contents to self.screen"""
		for n in self.iterable:
			self.screen.addstr(f"{n}:{self.atr(n)}\n", self.COLOR_MAP.get('text'))
		self.screen.refresh(0, 0, self.topy, self.leftx, self.boty, self.rightx)

	@log
	def draw_content(self):
		pass

	@log
	def close(self):
		"""Close the window"""
		# Does not work!
		pass
		#self.screen.clear()
		#self.screen.refresh()
	@log
	def _define_colors(self):
		"""A function to define custom colors. TODO."""
		pass

	@log
	def _calculate_size(self):
		"""Method run by create_window to calculate height and width"""
		height = self.atr('height') if self.atr('height') is not None else -1
		width = self.atr('width') if self.atr('width') is not None else -1
		vborder = self.atr('vborder') if self.atr('vborder') is not None else -1
		hborder = self.atr('hborder') if self.atr('hborder') is not None else -1
		# Height calculations:
		# TODO: Check else statements for truthiness
		if height == -1  and vborder == -1: # No border / No height case
			self.height = curses.LINES
		elif height == -1  and vborder >= 0: # Border only case
			self.height = curses.LINES - (2 * vborder)
		elif height > 0 and vborder == -1: # Height only case
			self.height = height
		else: # Error case: cannot have height and border
			raise ValueError("Can not define a custom height AND vertical border or height=0.")
		# Width calculations:
		# TODO: Check else statements for truthiness
		if width == -1 and hborder == -1: # No border / No height case
			self.width = curses.COLS
		elif width == -1 and hborder >= 0: # Border only case
			self.width = curses.COLS - (2 * hborder)
		elif width > 0 and hborder == -1: # Height only case
			self.width = width
		else: # Error case: cannot have height and border
			raise ValueError("Can not define a custom width AND horizontal borders, or width=0.")

	@log
	def _calculate_window_valign(self):
		"""Method run by create_window() to calculate topy and boty for draw_window()"""
		# Note: assignment of -1 is to prevent type errors when comparing int to nonetype
		topy = self.atr('topy') if self.atr('topy') is not None else -1
		boty = self.atr('boty') if self.atr('boty') is not None else -1
		valign = self.atr('valign')
		if topy >= 0 and boty >= 0:
			self.topy = topy
			self.boty = boty
		if valign == 'center' or valign == None:
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
		leftx = self.atr('leftx') if self.atr('leftx') is not None else -1
		rightx = self.atr('rightx') if self.atr('rightx') is not None else -1
		halign = self.atr('halign')
		if leftx >= 0 and rightx >= 0:
			self.leftx = leftx
			self.rightx = rightx
		if halign == 'center' or halign == None:
			center = math.floor(curses.COLS/2) # Always move left 1 from center if odd!
			self.leftx = center - math.floor(self.width/2) # Alwas move left 1!
			self.rightx = center + math.ceil(self.height/2) # Always move left 1!
		if halign == 'left':
			self.leftx = 0
			self.rightx = 0 + self.width - 1
		if halign == 'right':
			self.leftx = curses.COLS - 1
			self.rightx = curses.COLS - width

	@log
	def _map_colors(self):
		"""Looks through self.atr, grabbing all attributes with 'color' inside
		and then mapping them to a color pair number."""
		for atr in self.atr_dict: # Loop through self.atr
			if "color" in atr: # Ensure only grab color attributes
				color_key = atr.split('_')[0] # Extract key from string
				pair_num = self.COLOR_MAP.get(color_key)
				color_value = self.atr(color_key)
				if isinstance(color_value, int): # Default background is black
					curses.init_pair(pair_num, color_value, self.DEFAULT_BACK)
				elif color_value is None: # Default color is white if no color for key
					curses.init_pair(pair_num, self.DEFAULT_TEXT, self.DEFAULT_BACK)
				else: # Apply selected colors
					curses.init_pair(pair_num, *color_value)
				self.colors.update({color_key:pair_num})

def main(stdscr):
	"""
	A method for testing the view
	"""
	listview = ListView()
	listview.screen.getch()
	return 0

if __name__ == "__main__":
	curses.wrapper(main)
	print("Success!")
