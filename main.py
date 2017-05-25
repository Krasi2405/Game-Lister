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
		release_dates = get_info_as_json("https://igdbcom-internet-game-database-v1.p.mashape.com/release_dates/?fields=*&filter[date][gte]={}&limit=50&order=date:asc".format(int(curr_time)))
		for release_date in release_dates:
			game_name = get_info_as_json("https://igdbcom-internet-game-database-v1.p.mashape.com/games/{}?fields=name".format(release_date['game']))
			try:
				print("Release Date: {} - Unix Timestamp: {} - Game Name: {}\n\n".format(release_date['human'], release_date['date'], game_name[0]['name']))
			except:
				print("Couldnt print information for game with id: {}".format(release_date['game']))
	elif cmd == "id":
		id = int(input("Enter the id of the game: "))
		print(get_info_as_json("https://igdbcom-internet-game-database-v1.p.mashape.com/games/{}?fields=name".format(id)))
	else:
		print("Feeling lost? Type 'help' to see the help menu!")

