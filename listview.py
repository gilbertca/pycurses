import curses
from utils import log
from baseview import AbstractBaseView

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
	def draw_window(self):
		"""Render background, draw text, and then refresh screen."""
		self.screen.bkgd(".", curses.color_pair(self.controller.colors.get("background_color")))
		vpadding,hpadding = self._get_padding()
		lines_written = 0
		for item in self.iterable:
			color = curses.color_pair(self.determine_color(item))
			self.screen.addstr(lines_written+vpadding,hpadding,f"{item}:{self.atr(item)}\n", color)
			lines_written += 1
		self.screen.refresh(0, 0, self.topy, self.leftx, self.boty, self.rightx)

	@log
	def determine_color(self, item):
		"""
		Method to run checks on 'string' to return a color
		THIS CURRENT CODE IS TEMPORARY
		"""
		if "c" in item:
			return self.controller.get_color("important_color")
		else:
			return self.controller.get_color("text_color")
