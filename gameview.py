import curses
from utils import log
from baseview import AbstractBaseView
from listview import ListView
from controller import Controller

class GameView(AbstractBaseView):
	"""
	A sample game to demonstrate the abilities of pycurses.
	"""

	def draw_window(self):
		self.draw_background()
		vpadding,hpadding = self._get_padding()
		self.add_string("Hello, world.")
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

	def 

class GameController(Controller):
	"""
	Inherits from controller, and add's custom methods to FUNCTIONS_DICT
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.FUNCTIONS_DICT.update({
			'u' : self.use_item	
		})

	def use_item(self):
		"""
		Swaps focus to the inventory, and lets the player *use* an item
		"""
		# Hard coded name of inventory view:
		ITEM_VIEW_NAME = "inventory_view"
		view = self.views(ITEM_VIEW_NAME) # Get view
		

