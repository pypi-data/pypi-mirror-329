
from egyptian.generators import *

class Person:
	def __init__(self, language: str=None,gender: str=None, name_length: int=None,age: int=None,name: str=None,city: str=None,job_title:str=None,phone:str=None,
	             user_name:str=None,email:str=None,national_id:str=None,
	             phone_carrier:str=None,phone_start_with:str=None, user_name_lenght:int=None,birth_day=None,birth_month=None,birth_year=None,email_ends_with=None):
		# Store only user-provided arguments (ignore None values)
		self.user_provided_args = {k: v for k, v in locals().items() if k != 'self' and v is not None}
		if not name_length:
			name_length = 2
		if not user_name_lenght:
			user_name_lenght = 15
		if not language:
			self.language = choice(languages)
		else:
			language_check(language)
			self.language = language
		if not gender:
			if self.language.lower().startswith('ar'):
				self.gender = choice(arabic_genders)
			else:
				self.gender = choice(english_genders)
		else:
			gender_check(gender)
			self.gender = gender
			if self.language.lower().startswith('ar'):
				if gender in male_genders:
					self.gender = 'ذكر'
				else:
					self.gender = 'أنثي'
			else:
				if gender in male_genders:
					self.gender = 'male'
				else:
					self.gender = 'female'
		self.name_length = name_length
		if birth_year and age:
			raise Exception("You can't pass both birth_year and age")
		if not age:
			age = randint(0, 100)
			temp_age = age
			if self.language.lower().startswith('ar'):
				age = convert_to_arabic_numerals(str(age))
		else:
			temp_age = age
		self.age = age
		if not birth_year:
			birth_year = datetime.now().year - temp_age
			if self.language.lower().startswith('ar'):
				birth_year = convert_to_arabic_numerals(str(birth_year))
		self.birth_year = birth_year
		if not birth_month:
			birth_month = randint(1, 12)
			if self.language.lower().startswith('ar'):
				birth_month = convert_to_arabic_numerals(str(birth_month))
		self.birth_month = birth_month
		if not birth_day:
			birth_day = randint(1, 30)
			if self.language.lower().startswith('ar'):
				birth_day = convert_to_arabic_numerals(str(birth_day))
		self.birth_day = birth_day
		if not name:
			name = generate_name(language=self.language,gender=self.gender,name_length=self.name_length)
		self.name = name
		if not city:
			city = generate_city(language=self.language)
		self.city = city
		if not job_title:
			job_title = generate_job_title(language=self.language,gender=self.gender)
		self.job_title = job_title
		if not phone_carrier:
			self.phone_carrier = choice(phone_carriers)
		else:
			phone_carrier_check(phone_carrier)
			self.phone_carrier = phone_carrier
		if not phone_start_with:
			if self.language.lower().startswith('ar'):
				self.phone_start_with = choice(arabic_phone_start_withs)
			else:
				self.phone_start_with = choice(english_phone_start_withs)
		else:
			phone_start_with_check(phone_start_with)
			self.phone_start_with = phone_start_with
		if not phone:
			phone = generate_phone(language=self.language,phone_carrier=self.phone_carrier,phone_start_with=self.phone_start_with)
		self.phone = phone
		self.user_name_length = user_name_lenght
		if not user_name:
			user_name = generate_user_name(language=self.language,user_name_length=self.user_name_length,name=self.name)
		self.user_name = user_name
		if email and email_ends_with:
			raise Exception("You can't pass both email and email_ends_with")
		if not email_ends_with:
			self.email_ends_with = choice(email_ends_withs)
		else:
			email_ends_with_check(email_ends_with)
			self.email_ends_with = email_ends_with
		if not email:
			email = f"{self.user_name}@{self.email_ends_with}"
		self.email = email
		if not national_id:
			national_id = generate_national_id(language=self.language,birth_day=self.birth_day,birth_month=self.birth_month,birth_year=self.birth_year,gender=self.gender)
		self.national_id = national_id
	def update_name(self,language=None,name_length=None,gender=None):
		data = {"language":self.language,"gender":self.gender,"name_length":self.name_length}
		if language:
			data["language"] = language
		if name_length:
			data["name_length"] = name_length
		if gender:
			data["gender"] = gender
		name = generate_name(**data)
		self.name = name
		return self.name

	def update_user_name(self,language=None,user_name_length=None,name=None):
		data = {"language": self.language, "user_name_length": self.name_length,"name":self.name}
		if language:
			data["language"] = language
		if user_name_length:
			data["user_name_length"] = user_name_length
		if name:
			data["name"] = name
		user_name = generate_user_name(**data)
		self.user_name = user_name
		return self.user_name
	def update_job_title(self,language=None,gender=None):
		data = {"language": self.language, "gender": self.gender}
		if language:
			data["language"] = language
		if gender:
			data["gender"] = gender
		job_title = generate_job_title(**data)
		self.job_title = job_title
		return self.job_title

	def update_email(self,language=None,user_name_length=None,name=None):
		data = {"language": self.language, "user_name_length": self.user_name_length,"name":self.name}
		if language:
			data["language"] = language
		if name:
			data["name"] = name
		if user_name_length:
			data["user_name_length"] = user_name_length
		user_name = generate_user_name(**data)
		self.email = f"{user_name}@{self.email_ends_with}"
		return self.email
	def update_national_id(self,language=None,birth_day=None,birth_month=None,birth_year=None,gender=None):
		data = {"language": self.language, "gender": self.gender,"birth_day": self.birth_day,"birth_month": self.birth_month,"birth_year": self.birth_year}
		if language:
			data["language"] = language
		if birth_day:
			data["birth_day"] = birth_day
		if birth_month:
			data["birth_month"] = birth_month
		if birth_year:
			data["birth_year"] = birth_year
		if gender:
			data["gender"] = gender
		national_id = generate_national_id(**data)
		self.national_id = national_id
		return self.national_id
	def update_phone(self,language=None,phone_carrier=None,phone_start_with=None):
		data = {"language": self.language, "gender": self.gender, "name_length": self.name_length}
		if language:
			data["language"] = language
		if phone_carrier:
			data["phone_carrier"] = phone_carrier
		if phone_start_with:
			data["phone_start_with"] = phone_start_with
		phone = generate_phone(**data)
		self.phone = phone
		return self.phone
	def translate_name(self):
		translated_name = ""
		for name in self.name.split(" "):
			name = translate_name(name)
			translated_name += f"{name} "
		self.name = translated_name
		return self.name
	def translate_job_title(self):
		translated_job_title = translate_job_title(self.job_title)
		self.job_title = translated_job_title
		return self.job_title
	def translate_gender(self):
		translated_gender = translate_gender(self.gender)
		self.gender = translated_gender
		return self.gender
	def translate_city(self):
		translated_city = translate_city(self.city)
		self.city = translated_city
		return self.city
	def translate_phone(self):
		translated_phone = translate_number(self.phone)
		self.phone = translated_phone
		return self.phone
	def translate_national_id(self):
		translated_national_id = translate_number(self.national_id)
		self.national_id = translated_national_id
		return self.national_id
	def translate_birth_year(self):
		translated_birth_year = translate_number(self.birth_year)
		self.birth_year = translated_birth_year
		return self.birth_year
	def translate_birth_month(self):
		translated_birth_month = translate_number(self.birth_month)
		self.birth_month = translated_birth_month
		return self.birth_month
	def translate_birth_day(self):
		translated_birth_day = translate_number(self.birth_day)
		self.birth_day = translated_birth_day
		return self.birth_day


	def get_all(self,number_of_persons:int=1):
		if number_of_persons == 1:
			result = deepcopy(self.__dict__)
			filter_result(result)
			return {**result}
		else:
			persons = []
			data = self.user_provided_args
			for i in range(number_of_persons):
				person = Person(**data)
				result = deepcopy(person.__dict__)
				filter_result(result)
				persons.append(result)
			return persons

