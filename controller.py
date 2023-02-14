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

	def add_view(self, view_dict):
		self.views_dict.update(view_dict)

	def get_view(self, view_name):
		return self.views(view_name)

	def map_colors(self):
		pass
