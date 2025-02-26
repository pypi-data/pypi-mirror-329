from egyptian.__init__ import *
class IDParser:

	@staticmethod
	def validate_id(id_number):
		if not id_number.isdigit() or len(id_number) != 14:
			raise ValueError("ID Number Must Be 14 Digits Long.")

	@staticmethod
	def extract_birth_date(id_number):
		century_code = id_number[0]
		year = id_number[1:3]
		month = id_number[3:5]
		day = id_number[5:7]

		if century_code == '2':
			birth_year = '19' + year
		elif century_code == '3':
			birth_year = '20' + year
		else:
			raise ValueError("Invalid century code in ID")

		try:
			birth_date = datetime.datetime.strptime(f"{birth_year}-{month}-{day}", "%Y-%m-%d").date()
		except ValueError:
			raise ValueError("Invalid date in ID.")

		return birth_date

	@staticmethod
	def extract_governorate(id_number):
		governorate_code = id_number[7:9]
		return IDParser.governorate_map.get(governorate_code, "Unknown Governorate")

	@staticmethod
	def extract_gender(id_number):
		serial_number = int(id_number[9:13])
		return 'Male' if serial_number % 2 != 0 else 'Female'

	@staticmethod
	def calculate_age_components(birth_date):
		today = datetime.date.today()
		years = today.year - birth_date.year
		months = today.month - birth_date.month
		days = today.day - birth_date.day

		if days < 0:
			months -= 1
			days += (birth_date + datetime.timedelta(days=30)).day
		if months < 0:
			months += 12
			years -= 1

		return years, months, days