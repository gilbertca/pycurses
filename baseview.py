import curses
import math
from utils import log


class AbstractBaseView:
	"""
	An abstraction from which all views will inherit.
	Contains methods which must be overloaded by its children
	"""
	def __init__(self, controller, **atr):
		# Constant values:
		self.controller = controller # References parent controller
		self.atr_dict = atr # Contains all attributes
		self.atr = self.atr_dict.get # use self.atr('key') saving typing .get()
		self.FUNCTIONS_DICT = {
			
		}
		self.function = self.FUNCTIONS_DICT.get
		self.BACKGROUND_FILL = self.atr('background_fill') if atr.get('background_fill') is not None else ' '

	@log
	def add_string(self, string, y=None, x=None, *args, **kwargs):
		# NEEDS STATEMENT FOR NONEXISTENT X OR Y?
		if y is None or x is None:
			self.screen.addstr(string, *args, **kwargs)
		elif y >= 0 and x >= 0:
			self.screen.addstr(y, x, string, *args, **kwargs)

	@log
	def create_window(self):
		"""Creates a pad or window object based on given parameters"""
		self._calculate_size()
		self._calculate_window_valign()
		self._calculate_window_halign()
		self.screen = curses.newpad(self.height, self.width)
	
	@log
	def determine_color(self, string):
		"""
		To be overloaded by child.
		"""
		raise Exception(f"This method must be overloaded by it's child.")

	@log
	def draw_background(self):
		"""
		Does the absurd calls required to draw the background.
		"""
		background_attributes  = (
			self.BACKGROUND_FILL, # Get the 'fill' character
			# This next call returns the background color... unfortunately.
			curses.color_pair(self.controller.colors.get(self).get("background_color"))
		)
		self.screen.bkgd(*background_attributes)

	@log
	def draw_window(self):
		"""
		To be overloaded by child.
		"""
		raise Exception(f"This method must be overloaded by it's child.")

	@log
	def interact(self): """
		Method which will check for internal functions first,
			and return the key_press if no function is found.
		Maybe the ability to pass commands to multiple views
			at a time, or allow controller access to these keys?
		"""
		key_press = self.screen.getch()
		function = self.function(key_press)
		if function is None: # If no function found, return keypress:
			return key_press
		else: # Otherwise there is a function, and it should be run:
			function()

	@log
	def refresh_screen(self):
		self.screen.refresh(0, 0, self.topy, self.leftx, self.boty, self.rightx)

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
			self.topy = curses.LINES - self.height
			self.boty = curses.LINES - 1

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
