import arrow
import datefinder
import datetime
import parsedatetime
from pytime import pytime
from pprint import pprint
from humandate import parse_date
import pytz


class GetTime(object):
	"""
		Recovers time which is in a string format and converts it to a datetime object
		Example,
			I will meet you in 4 days. -- converts to datetime.datetime(2018, 4, 26, 20, 8, 35, 309208)
		Recovers multiple times specified as well.

		params:
			text: Text from which time needs to be extracted
			zone: Time zone to convert datetime object to
	"""
	def __init__(self, text, zone = pytz.timezone("Asia/Calcutta")):
		self.text = text
		self.possible_dates = []
		self.zone = zone

	# Finds for most formats
	def get_time(self):
		"""
			Recovers times from the sentence

			params : None
			returns : dict object with possible dates and text
		"""
		print("Get time")
		return_dict = {
			"possible_dates" : self.possible_dates,
			"text" : self.text
		}
		print(list(datefinder.find_dates(self.text)))
		if self.possible_dates == []:
			temp = list(datefinder.find_dates(self.text))
			for item in temp:
				return_dict['possible_dates'].append(item.astimezone(self.zone))
			return return_dict
		else:
			for item in list(datefinder.find_dates(self.text)):
				self.possible_dates.append(item)
			return_dict['possible_dates'] = self.possible_dates

	def get_on_fail(self):
		"""
			On fail of the above function this can be called to find time with typos

			params : None
			returns : dict object with possible dates and text
		"""
		print("On Fail")
		return_dict = {
			'possible_dates' : self.possible_dates,
			'text' : self.text
		}
		p = parsedatetime.Calendar()
		return_dict['possible_dates'].append(p.parseDT(self.text)[0].astimezone(self.zone))
		return return_dict

	# Handles dates times like <next month>
	def second_fail(self):
		"""
			Recognises times like next month, tomorrow etc.

			params : None
			returns : dict object with possible dates and text
		"""
		print("Second Fail")
		return_dict = {
			'possible_dates' : self.possible_dates,
			'text' : self.text
		}
		return_dict['possible_dates'].append(parse_date(self.text).astimezone(self.zone))
		return return_dict

	# Detects for improper formats like <21dayz2weks, 23month3dy29minu>
	def third_fail(self):
		"""
			Recognises times of formats 21dayz3weks. And other improper formated dates

			params : None
			returns : dict object with possible dates and text
		"""
		print("Third Fail")
		return_dict = {
			'possible_dates' : self.possible_dates,
			'text' : self.text
		}
		return_dict['possible_dates'].append(pytime.after(datetime.datetime.now().astimezone(self.zone), self.text))
		return return_dict

	def __call__(self):
		"""
			Object call method to find all the dates in a text passed as object parameter

			params : text to be converted to datetime
			returns : dict object with possible dates and text if all cases fai, returns datetime.datetime.now()
					as possible dates
		"""
		try:
			ret_dict = self.get_time()
			if ret_dict['possible_dates'] == []:
				ret_dict = self.get_on_fail()
				if ret_dict['possible_dates'] == []:
					ret_dict = self.second_fail()
					if ret_dict['possible_dates'] == []:
						ret_dict = self.third_fail()
			elif len(ret_dict['possible_dates']) == 0 or len(ret_dict['possible_dates']) > 1:
				ret_dict = {
					'possible_dates' : [],
					'text' : self.text
				}
				dates = []
				dates.append(self.get_time())
				dates.append(self.get_on_fail())
				dates.append(self.second_fail())
				dates.append(self.third_fail())

				for date in dates:
					for item in date['possible_dates']:
						if item not in ret_dict['possible_dict']:
							ret_dict['possible_dict'].append(item.astimezone(self.zone))

		except Exception as e:
			print(e)
			ret_dict = {
				'possible_dates' : [datetime.datetime.now().astimezone(self.zone)],
				'text' : self.text
			}

		return ret_dict
