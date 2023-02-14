from listview import ListView
from baseview import AbstractBaseView

class Controller:
	"""
	Controller needs to map colors in order to keep track of arbitrary number of color pairs.
	Controller needs to call draw methods for view objects
	"""
	def __init__(self, views_dict=None):
		self.views_dict = views_dict
		self.views = self.views_dict.get # Saves typing .get on every reference
		self.map_colors()

	def add_view(self, view_dict):
		self.views_dict.update(view_dict)

	def draw_view(self, view_name):
		self.views(view_name).create_window()
		self.views(view_name).draw_window()

	def get_view(self, view_name):
		return self.views(view_name)

	@log
	def map_colors(self):
		"""
		Links colors to color pair integers
		"""
		for view in self.views_dict: # Loop through self.views_dict
			for atr in view.atr_dict: # Loop through the attributes of each view
				if "color" in atr: # Color only contained by values which set colors
					color_value = view.atr(atr) # Get color list/string from view.atr
					pair_num = # Check length of list, assign next number based on list 
					if isinstance(color_value, list): # If list -> Assign [0] as fore and [1] as back
						# Need to relate list values to CURSES_COLOR_MAP
						colors = [view.CURSES_COLOR_MAP.get(color) for color in color_value]
						curses.init_pair(pair_num, *colors)
					elif isinstance(color_value, str): # If string -> Assign string as fore and back as view.DEFAULT_BACK
						# Need to relate string value to CURSES_COLOR_MAP
						# Consider moving the CURSES_COLOR_MAP to controller
						color = view.CURSES_COLOR_MAP.get(color_value)
						curses.init_pair(pair_num, color, view.DEFAULT_BACK)
					elif color_value is None: # If None -> Default white on black
						curses.init_pair(pair_num, view.DEFAULT_TEXT, view.DEFAULT_BACK)
