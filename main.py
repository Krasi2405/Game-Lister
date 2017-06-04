import pdb
import datetime
import sys
import os
import time
import msvcrt as m # Module that imports getch()
import requests
import pickle
import pdb

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


def display_main_menu_help():
	print("Type 'games' to enter the games menu.")
	print("Type 'companies' to enter the companies menu.")
	print("Type 'options' to change the viewing mode.")
	print("Type 'help' to see this again.")
	print("Type 'exit' to exit the program.")


def display_games_menu_help():
	print("Type 'search' to start searching for games.")
	print("Type 'upcoming' to see upcoming games.")
	print("Type 'id' to look for a game by its id.(Debugging Purposes Only)")
	print("Type 'popular' to see the most popular games.")
	print("Type 'favourites' to see your favourite games.")
	print("Type 'help' to see this again.")
	print("Type 'exit' to exit the menu.")


def display_company_menu_help():
	print("Type 'search' to look for companies by name.")
	print("Type 'games' to look for games made by a certain company.")
	print("Type 'help' to see this again.")
	print("Type 'exit' to exit the menu.")


def get_saved_menu_mode():
	try:
		file = open("menu_mode.pickle", "rb")
		return pickle.load(file)
	except EOFError:
		pass


def save_menu_mode(menu_mode):
	file = open("menu_mode.pickle", "wb")
	pickle.dump(menu_mode, file)


def choose_from_options(options_list, message = "Choose option: "):
	if len(options_list) == 0:
		print("No items to choose from!")
		return 0
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
			clear()
			return options_list[i]
		elif(ch == b'\x1b'):
			clear()
			return None
		clear()


def normal_review_menu(obj_list, return_favourites):
	if return_favourites:
		favourites = set()
		last_obj = None
	while(True):
		description = choose_from_options([obj.short_review() for obj in obj_list])
		for obj in obj_list:
			if description == obj.short_review():
				print("-" * os.get_terminal_size()[0])
				print(obj.long_review())
				print("-" * os.get_terminal_size()[0])
				if return_favourites:
					last_obj = obj

		print("\n\nPress the escape key to exit this menu. Press 'f' to add this to your favourites.")
		ch = m.getch()
		if ch == b'\x1b':
			if return_favourites:
				return favourites
			else:
				return None
		elif ch == b'f':
			if return_favourites:
				favourites.add(last_obj)
		clear()


def alternative_review_menu(obj_list, return_favourites):
	obj_list = list(obj_list)
	if return_favourites:
		favourites = set()
	current_index = 0
	while(True):
		clear()
		
		print("-" * os.get_terminal_size()[0])
		print(obj_list[current_index].long_review())
		print("-" * os.get_terminal_size()[0])
		print("\nPress 'w' to move up or press 's' to move down the entry list.")
		if return_favourites:
			print("Press 'f' to favourite this object.")
		print("Press the escape button to exit this menu.")

		ch = m.getch()
		if ch == b's' and current_index > 0:
			current_index -= 1
		elif ch == b'w' and current_index < len(obj_list) - 1:
			current_index += 1
		elif ch == b'\x1b':
			if return_favourites:
				return favourites
			else:
				return None
		elif ch == b'f':
			if return_favourites:
				favourites.add(obj_list[current_index])
				clear()
				print("{} has been added to favourites".format(obj_list[current_index].name))
				m.getch()
				clear()
				
	clear()


def menu_print(menu_mode, obj_list, return_favourites = True):
	if menu_mode == "normal":
		return normal_review_menu(obj_list, return_favourites)
	elif menu_mode == "alternative":
		return alternative_review_menu(obj_list, return_favourites)

def update_set_by_obj_id(set1, set2):
	for obj2 in set2:
		add = True
		for obj1 in set1:
			if obj1.id == obj2.id:
				add = False
				break
		if add:
			set1.add(obj2)
	return set1


if __name__ == "__main__":
	favourite_games = set()
	favourite_companies = set()
	http_handler = HttpRequestHandler()
	os.system("chcp 65001") # Set the encoding to utf-8
	menu_mode = get_saved_menu_mode()
	clear()

	# Ask the user to set the menu_mode if it isn't set already
	# In ideal conditions should only ever execute on the program's first execution.
	if(not menu_mode):
		print("Menu mode not found. Please set it.")
		menu_mode = choose_from_options(["normal", "alternative"])
		print("Setting menu mode to {}".format(menu_mode))
		clear()

	display_main_menu_help()

	while(True):
		cmd = input("Enter command: ")
		clear()
		if "help" in cmd:
			display_main_menu_help()
		elif cmd == "games":
			display_games_menu_help()
			while(True):
				cmd = input("Enter command: ")
				clear()
				if "help" in cmd:
					display_games_menu_help()
				elif cmd == "popular":
					games_list = http_handler.get_most_popular_games();
					favourites = menu_print(menu_mode, games_list)
					update_set_by_obj_id(favourite_games, favourites)
				elif cmd == "search":
					while(True):
						argument = input("Enter your search query or 'exit' to exit: ")
						if argument.lower() == "exit" or argument.lower() == 'e':
							break
						games_list = http_handler.search_games(argument)
						favourites = menu_print(menu_mode, games_list)
						update_set_by_obj_id(favourite_games, favourites)

				elif cmd == "upcoming":
					games_list = http_handler.get_upcoming_games()
					favourites = menu_print(menu_mode, games_list)
					update_set_by_obj_id(favourite_games, favourites)

				elif cmd == "favourites":
					if(len(favourite_games) > 0):
						menu_print(menu_mode, list(favourite_games), False)
					else:
						print("No favourite games!")

				elif cmd == "id":
					print("Debugging purposes only!")
					id = int(input("Enter the id of the game: "))
					info = http_handler._get_info_as_json("https://igdbcom-internet-game-database-v1.p.mashape.com/games/{}?fields=*".format(id))
					print(info)

				elif cmd == "e" or cmd == "exit":
					break
				else:
					print("Type 'help' to see the help menu!")

		# Work put on hold until i have finished the games options.
		elif cmd == "companies":
			display_company_menu_help()
			while(True):
				cmd = input("Enter command: ")
				clear()
				if "help" in cmd:
					display_company_menu_help()
				elif cmd == 'games':
					id = input("Enter the id of the publisher you would like to see")
					games_list = http_handler.get_games_from_publisher_by_id(id)
					games_list += http_handler.get_games_from_developer(id)
					menu_print(menu_mode, games_list) if games_list else print("This publisher has not released any games yet!")

		
		elif cmd == "options":
			menu_mode = choose_from_options(["normal", "alternative"])

		elif cmd == "e" or cmd == "exit":
			save_menu_mode(menu_mode)
			break
		else:
			print("Type 'help' to see the help menu!")

