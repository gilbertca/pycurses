from main.py import ListView


class Controller:
	"""
	Controller needs to map colors in order to keep track of arbitrary number of color pairs.
	"""
	def __init__(self, **views):
		self.view_dict = {}
		for view in views:
			self.view_list.update(view)

	def add_view(self, view):
		self.view_list.update(view)
