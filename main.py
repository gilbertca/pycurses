import curses
import math
import logging
from argparse import ArgumentParser

# Logging setup:
logging.basicConfig(filename='pycurses.log', filemode='w', level=logging.DEBUG)

class Focusable:
	"""An inheritable abtract class which allows a window object to take focus"""
	pass

class Scrollable:
	"""
	An inheritable abstract class which allows a window object to scroll
	Objects should override the .draw() method
	"""
	pass

def errorh(function):
	"""Decorator to handle simple try/except statements"""
	def errh(*args, **kwargs):
		try:
			function(*args, **kwargs)
		except Error as e:
			logging.warning("Error {e}")
					
	return errh

class ListView:
	"""
	A class to display a curses list given a window/pad object, and a list
	Also accepts several key word parameters
	The object can be created as a list, or as a pad
	Like half, quarter, third, etc.
	Also top, bottom, left right, center
	Width can be a keyword string, or a numeric value
	"""
	def __init__(self, iterable, **atr):
		# Required setup:
		self.iterable = iterable
		self.atr_dict = atr
		self.atr = self.atr_dict.get # self.atr('key') returns the value, saving typing .get()
		# Temporary parameters:
		self._calculate_size()
		self._calculate_window_valign()
		# Steps to create window:
		self.define_colors() # init color pairs for use using provided string keywords
		self.create_window() # create a pad of fixed dimensions based on string keywords
		self.draw_window() # draw text to screen using given colors

	def define_colors(self):
		self.has_colors = 1
		curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

	def create_window(self):
		"""Creates a pad or window object based on given parameters"""
		self._calculate_size()
		self.screen = curses.newpad(self.height, self.width)

	def _calculate_size(self):
		"""Method run by create_window to calculate height and width"""
		height = self.atr('height') if self.atr('height') is not None else -1
		width = self.atr('width') if self.atr('width') is not None else -1
		vborder = self.atr('vborder') if self.atr('vborder') is not None else -1
		hborder = self.atr('hborder') if self.atr('hborder') is not None else -1
		# Height calculations:
		if height == -1  and vborder == -1:
			self.height = curses.LINES
		elif height == -1  and vborder >= 0:
			self.height = curses.LINES - (2 * vborder)
		elif height > 0 and vborder == -1:
			self.height = height
		else:
			raise ValueError("Can not define a custom height AND vertical padding or height=0.")
		# Width calculations:
		if width == -1 and hborder == -1:
			self.width = curses.COLS
		elif width == -1 and hborder >= 0:
			self.width = curses.COLS - (2 * hborder)
		elif width > 0 and hborder == -1:
			self.width = width
		else:
			raise ValueError("Can not define a custom width AND horizontal borders, or width=0.")

	def _calculate_window_valign(self):
		"""Method run by XXX to calculate topy and boty for draw_window()"""
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

	def _calculate_halign(self):
		"""Method run by XXX to calculate topx and botx for draw_window()"""
		pass

	def draw_window(self):
		"""Draw the contents to self.screen"""
		for n in self.iterable:
			self.screen.addstr(f"{n}\n")
		if self.has_colors:
			self.screen.bkgd(' ', curses.color_pair(1))
		self.screen.refresh(0, 0, self.topy, 10, self.boty, 30)

	def draw_content(self):
		pass	

	def close(self):
		"""Close the window"""
		# Does not work!
		pass
		#self.screen.clear()
		#self.screen.refresh()

def main(stdscr):
	"""
	A method for testing the view
	"""
	# Creating bogus data
	valign = 'center'
	height = width = 20
	ind = 0
	interesting_string = f"Height is {height} and width is {width}"
	iterable = interesting_string.split(" ")
	# Running actual code:
	listview = ListView(iterable, 
		height=height, width=width,
		valign=valign
	)
	listview.screen.getch()
	stdscr.refresh()
	noneview = ListView("NONEVIEW", 
		height=None, width=None,
		valign=None, halign=None,
		back_color=None, fore_color=None,
	)
	noneview.screen.getch()
	stdscr.touchwin()
	stdscr.refresh()
	noneview.screen.getch()
	return 0

if __name__ == "__main__":
	curses.wrapper(main)
	print("Success!")
