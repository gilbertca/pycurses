import curses
import math
import logging
from utils import parse_json, log
from baseview import AbstractBaseView

lass ListView(AbstractBaseView):
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
