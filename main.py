import curses
from listview import ListView
from controller import Controller
from utils import parse_json

JSON_FILE1 = "json/listview1.json"
JSON_FILE2 = "json/listview2.json"
def main(stdscr):
	"""
	A method for testing the view
	"""
	controller = Controller()
	listatr1 = parse_json(JSON_FILE1)
	listview1 = ListView(controller, listatr1)
	dict = {"listview1":listview1}
	controller.add_view(dict)
	controller.draw_view("listview1")
	controller.get_view("listview1").screen.getch()
	return 0

if __name__ == "__main__":
	curses.wrapper(main)
