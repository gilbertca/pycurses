import curses
from utils import log
from baseview import AbstractBaseView
from listview import ListView

class GameView(AbstractBaseView):
	"""
	A sample game to demonstrate the abilities of pycurses.
	"""

	def draw_window(self):
		self.draw_background()
		vpadding,hpadding = self._get_padding()
		self.screen.addstr("Hello, world.")
		self.refresh_screen()

	def determine_color(self, item):
		return self.controller.get_color(self, "text_color")

class InventoryView(ListView):
	"""
	An extension of the ListView view to represent 
		the character's *inventory*.
	"""
	starting_inventory = {
		'torch':1,
		'gold':5,
		'sword':1,
		'potion':1
	}
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# This terrible line creates a nice string from inventory:
		self.iterable = [f"{item.capitalize()} {InventoryView.starting_inventory.get(item)}" for item in InventoryView.starting_inventory]
