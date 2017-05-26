import requests
import pdb
import igdb
import datetime
import sys
import os
import time

API_KEY = 'pXHeOVmmdzmshLbYBk9pW0cdcascp1vka8ajsngrzxD6GmIAVD'
API_KEY_HEADER = {'X-Mashape-Key': API_KEY}
API_ACCESS_HEADER = {'Accept': 'application/json'}

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
	print("Type 'id' to look for a game by its id.")


def get_info_as_json(http_address):
    r = requests.get(http_address, headers= {**API_KEY_HEADER, **API_ACCESS_HEADER})
    return r.json()


def get_most_popular_games():
	return get_info_as_json("https://igdbcom-internet-game-database-v1.p.mashape.com/games/?fields=name,popularity&order=popularity:desc")


def search_games(search_phrase, limit = 10):
	address = "https://igdbcom-internet-game-database-v1.p.mashape.com/games/?fields=name&limit={}&offset=0&order=release_dates.date%3Adesc&search={}".format(limit, search_phrase)
	return get_info_as_json(address)


os.system("chcp 65001") # Set the encoding to utf-8
clear()
display_help()
while(True):
	cmd = input("Enter command: ")
	clear()
	if cmd == "help":
		display_help()
	elif cmd == "search":
		while(True):
			argument = input("Enter your search query: ")
			if argument.lower() == "exit" or argument.lower() == 'e':
				break
			games = search_games(argument, 50);
			for game in games:
				print("--------------------------------------------")
				for key in game:
					print(u"{}: {}".format(key, game[key]))
				print("--------------------------------------------\n")
	elif cmd == "upcoming":
		curr_time = 1495753635000 # 5/26/2017 In Unix time in miliseconds
		search = "https://igdbcom-internet-game-database-v1.p.mashape.com/games/?fields=name,release_dates&limit=50&filter[first_release_date][gte]={}&order=first_release_date:asc".format(curr_time)
		upcoming_games = get_info_as_json(search)
		for game in upcoming_games:
			try:
				print(u"Time: {} - Unix Timestamp: {} - Game Name: {}".format(
					game['release_dates'][0]['human'], game['release_dates'][0]['date'], game['name']))
			except TypeError:
				print("Couldnt print information for game with id: {}".format(game['id']))
				print(u"Printing raw info for game: \n{}".format(game))
	elif cmd == "id":
		id = int(input("Enter the id of the game: "))
		print(get_info_as_json("https://igdbcom-internet-game-database-v1.p.mashape.com/games/{}?fields=name".format(id)))
	else:
		print("Feeling lost? Type 'help' to see the help menu!")

