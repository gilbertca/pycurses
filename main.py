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
	listatr1 = parse_json(JSON_FILE1)
	listatr2 = parse_json(JSON_FILE2)
	listview1 = ListView(listatr1)
	listview2 = ListView(listatr2)
	listviewdict = {
		"listview1" : listview1,
		"listview2" : listview2
	}
	controller = Controller(listviewdict)
	listview1.screen.getch()
	return 0

if __name__ == "__main__":
	curses.wrapper(main)
