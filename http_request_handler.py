import requests
import time
from game import Game
from company import Company
from franchise import Franchise

class HttpRequestHandler:

	API_KEY = "pXHeOVmmdzmshLbYBk9pW0cdcascp1vka8ajsngrzxD6GmIAVD"
	API_KEY_HEADER = {'X-Mashape-Key': API_KEY}
	API_ACCESS_HEADER = {'Accept': 'application/json'}

	def _get_info_as_json(self, http_address):
		r = requests.get(http_address, headers= {**self.API_KEY_HEADER, **self.API_ACCESS_HEADER})
		return r.json()


	def get_upcoming_games(self):
		curr_time = int(time.time()) * 1000
		search = "https://igdbcom-internet-game-database-v1.p.mashape.com/games/?fields=name,release_dates,summary&limit=50&filter[first_release_date][gte]={}&order=first_release_date:asc".format(curr_time)
		upcoming_games = self._get_info_as_json(search)
		games_list = [Game(current_game) for current_game in upcoming_games]
		return games_list

	def get_most_popular_games(self):
		games = self._get_info_as_json("https://igdbcom-internet-game-database-v1.p.mashape.com/games/?fields=*&order=popularity:desc")
		games_list = [Game(current_game) for current_game in games]
		return games_list

	def search_games(self, search_phrase, limit = 10, offset = 0):
		address = "https://igdbcom-internet-game-database-v1.p.mashape.com/games/?fields=*&limit={}&offset={}&order=release_dates.date%3Adesc&search={}".format(limit, offset,search_phrase)
		return get_info_as_json(address)

	def get_games_from_pubisher(self, id):
		search = "https://igdbcom-internet-game-database-v1.p.mashape.com/games/?fields=*&filter[publishers][in]={}".format(id)
		games = self._get_info_as_json(search)
		games_list = [Game(current_game) for current_game in games]
		return games_list