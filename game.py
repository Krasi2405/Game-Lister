import time


class Game:


	# id is the id of the game in igdb's database
	# release_date is the release_date of the game in human format
	def __init__(self, game_info_dict):
		self.id = game_info_dict.get("id")
		self.name = game_info_dict.get("name")
		self.release_date = game_info_dict['release_dates'][0].get("human")
		self.summary = game_info_dict.get("summary")
		self.rating = game_info_dict.get("rating")

	def short_review(self):
		info = "{} - {}.".format(self.name, self.release_date)
		if self.rating:
			info += "Rated {}/100".format(self.rating)

		return info

	def long_review(self):
		info = self.short_review()
		info += "\n\n{}".format(self.summary)
		return info


