import pdb
import datetime
import sys
import os
import time
import msvcrt as m # Module that imports getch()
import requests

from game import Game
from company import Company
from franchise import Franchise

from http_request_handler import HttpRequestHandler


def clear():
	if sys.platform == "linux" or sys.platform == "linux2":
		os.system("clear")
	elif sys.platform == 'win32':
		os.system("cls")
	else:
		print("System {} not recognized!".format(sys.platform))


def display_help():
	print("Type 'help' to see this again.")
	print("Type 'search' to start searching for games.")
	print("Type 'upcoming' to see upcoming games.")
	print("Type 'options' to change the viewing mode.")
	print("Type 'id' to look for a game by its id.(Debugging Purposes Only)")
	print("Type 'popular' to see the most popular games.")
	print("Type 'publishers' to get a list of all the games made by a certain publisher.")
	print("Type 'exit' to exit the program.")


def get_saved_menu_mode():
	return None


def choose_from_options(options_list, message = "Choose option: "):
	i = 0
	while(True):
		print("{}".format(message))
		for option_index in range(len(options_list)):
			display = options_list[option_index]
			if(i == option_index):
				display += " - current"
			print(display)

		ch = m.getch()
		if(ch == b'w' and i > 0):
			i -= 1
		elif(ch == b's' and i < len(options_list) - 1):
			i += 1
		elif(ch == b'\r'):
			return options_list[i]

		clear()


def basic_review_print(obj_list):
	for obj in obj_list:
		print("-" * os.get_terminal_size()[0])
		print("{}".format(obj.long_review()))
		print("-" * os.get_terminal_size()[0] + "\n\n")


def normal_review_print(obj_list):
	while(True):
		description = choose_from_options([obj.short_review() for obj in obj_list])
		clear()
		for obj in obj_list:
			if description == obj.short_review():
				print("-" * os.get_terminal_size()[0])
				print(obj.long_review())
				print("-" * os.get_terminal_size()[0])

		print("\n\nPress the 'escape' key to exit this menu. Press anything else to continue.")
		cmd = m.getch()
		if cmd == b'\x1b':
			break
	clear()


def alternative_review_print(obj_list):
	current_index = 0
	while(True):
		clear()
		print("Press 'w' to move up or press 's' to move down the entry list.")
		print("-" * os.get_terminal_size()[0])
		print(obj_list[current_index].long_review())
		print("-" * os.get_terminal_size()[0])

		ch = m.getch()
		if(ch == b's' and current_index > 0):
			current_index -= 1
		elif(ch == b'w' and current_index < len(obj_list) - 2):
			current_index += 1
		elif(ch == b'\x1b'):
			break
	clear()


def menu_print(menu_mode, obj_list):
	if menu_mode == "basic":
		basic_review_print(obj_list)
	elif menu_mode == "normal":
		normal_review_print(obj_list)
	elif menu_mode == "alternative":
		alternative_review_print(obj_list)

if __name__ == "__main__":
	http_handler = HttpRequestHandler()
	os.system("chcp 65001") # Set the encoding to utf-8
	menu_mode = get_saved_menu_mode()
	clear()

	# Ask the user to set the menu_mode if it isn't set already
	if(not menu_mode):
		print("Menu mode not found. Please set it.(Currently only basic is available)")
		menu_mode = choose_from_options(["basic", "normal", "alternative"])
		print("Setting menu mode to {}".format(menu_mode))
		clear()

	display_help()

	while(True):
		cmd = input("Enter command: ")
		clear()
		if "help" in cmd:
			display_help()
		elif cmd == "popular":
			games_list = http_handler.get_most_popular_games();
			menu_print(menu_mode, games_list)
		elif cmd == "search":
			while(True):
				argument = input("Enter your search query: ")
				if argument.lower() == "exit" or argument.lower() == 'e':
					break
				games_list = http_handler.search_games(argument)
				menu_print(menu_mode, games_list)	
		elif cmd == "upcoming":
			games_list = http_handler.get_upcoming_games()
			menu_print(menu_mode, games_list)
		elif cmd == "publishers":
			id = input("Enter the id of the publisher you would like to see")
			games_list = http_handler.get_games_from_pubisher(id)
			menu_print(menu_mode, games_list) if games_list else print("No games found with this publisher.")
		elif cmd == "id":
			print("Debugging purposes only!")
			id = int(input("Enter the id of the game: "))
			info = http_handler._get_info_as_json("https://igdbcom-internet-game-database-v1.p.mashape.com/games/{}?fields=*".format(id))
			print(info)
		elif cmd == "options":
			menu_mode = choose_from_options(["basic", "normal", "alternative"])
		elif cmd == 'e' or cmd == 'exit':
			break
		else:
			print("Feeling lost? Type 'help' to see the help menu!")

