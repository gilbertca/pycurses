import curses
from utils import log
from baseview import AbstractBaseView

class GameView(AbstractBaseView):
	"""
	A sample game to demonstrate the abilities of pycurses.
	"""

	def draw_window(self):
		self.draw_background()
		vpadding,hpadding = self._get_padding()

	def determine_color(self, item):
		return self.controller.get_color(self, "text_color")
