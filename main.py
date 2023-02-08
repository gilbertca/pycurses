import curses
import math
import logging
from utils import parse_json, log
from baseview import AbstractBaseView

class Focusable:
	"""An inheritable abtract class which allows a window object to take focus"""
	pass

class Scrollable:
	"""
	An inheritable abstract class which allows a window object to scroll
	Objects should override the .draw() method
	"""
	pass

class ListView(AbstractBaseView):
	"""
	A class to display a list given an arbitrary keyword list of attributes.
	A list of keywords can be found in 'keywords.txt'
	Also top, bottom, left right, center,
	Width can be a keyword string, or a numeric value.
	Note that some keyword configurations may overwrite each other
	"""
	# More to be added as more requirements are needed
	# Also need to be able to generate arbitrary color mappings
	# Need to define/declare variables regarding color pairs

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
		"""Render background, draw text, and then refresh screen."""
		self.screen.bkgd(self.BACKGROUND_FILL, curses.color_pair(2))
		padding = self.atr('padding') if self.atr('padding') else 0
		hpadding = self.atr('hpadding') if self.atr('hpadding') else 0
		vpadding = self.atr('vpadding') if self.atr('vpadding') else 0
		lines_written = 0
		for n in self.iterable:
			color = self._determine_color(n)
			if padding:
				self.screen.addstr(lines_written+padding,padding,f"{n}:{self.atr(n)}\n", color)
			else:
				self.screen.addstr(lines_written+vpadding,hpadding,f"{n}:{self.atr(n)}\n", color)	
			lines_written += 1
		self.screen.refresh(0, 0, self.topy, self.leftx, self.boty, self.rightx)

	@log
	def _determine_color(self, string):
		""" Method to run checks on 'string' to return a color
			Intended to be overloaded by child classes.
			*NOTE* ALL CODE CURRENTLY IN THIS METHOD IS TEMPORARY
		"""
		if "c" in string:
			color = self.color('important_color')
		else:
			color = self.color('text_color')
		return color

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
			self.leftx = curses.COLS - 1
			self.rightx = curses.COLS - width

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
				elif isinstance(color_value, str): # If string -> Assign string as fore and back as black
					# Need to relate string value to CURSES_COLOR_MAP
					color = self.CURSES_COLOR_MAP.get(color_value)
					curses.init_pair(pair_num, color, self.DEFAULT_BACK)
				elif color_value is None: # If None -> Default white on black
					curses.init_pair(pair_num, self.DEFAULT_TEXT, self.DEFAULT_BACK)

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
