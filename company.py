class Company:

	def __init__(self, company_info_dict):
		self.id = company_info_dict.get("id")
		self.name = company_info_dict.get("name")
		self.country = company_info_dict.get("country")
		self.website = company_info_dict.get("website")


	def short_review(self):
		info = u"{}. {}".format(self.id, self.name)
		info +=
		return info


	def long_review(self):
		info = self.short_review()
		# TO DO
		# Add more info