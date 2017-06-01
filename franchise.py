class Franchise:

	def __init__(self, franchise_info_dict):
		self.id = franchise_info_dict.get("id")
		self.name = franchise_info_dict.get("name")


	def short_review(self):
		info = u"{}. {}".format(self.id, self.name)
		return info

	def long_review(self):
		info = self.short_review()
		# TO DO
		# Add more info
