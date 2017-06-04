import time


class Game:
	# id is the id of the game in igdb's database
	# release_date is the release_date of the game in human format
	def __init__(self, game_info_dict):
		self.id = game_info_dict.get("id")
		self.name = game_info_dict.get("name")

		release_dates = game_info_dict.get('release_dates')
		if release_dates:
			self.release_date = release_dates[0]['human'] 
			self.unix_release_date = release_dates[0]['date']
		else:
			self.release_date = None
			self.unix_release_date = None

		if self.unix_release_date != None and self.unix_release_date < int(time.time() * 1000):
			self.is_released = True 
		else:
			if self.unix_release_date == None:
				self.is_released = True
			else:
				self.is_released = False

		self.summary = game_info_dict.get("summary")
		self.rating = game_info_dict.get("rating")
		

	def short_review(self):
		info = u"{}. {} - {}.".format(self.id, self.name, self.release_date)
		if self.rating:
			info += "\nRated {}/100".format(self.rating)

		return info

	def long_review(self):
		info = self.short_review()
		info += "\n{}".format(self.summary)
		return info


