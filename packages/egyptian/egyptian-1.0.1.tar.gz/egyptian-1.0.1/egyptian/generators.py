from egyptian.db import *
from egyptian.__init__ import *
def convert_to_arabic_numerals(english_number: str) -> str:
	translation_table = str.maketrans("".join(english_numerals), "".join(arabic_numerals))
	return english_number.translate(translation_table)
def convert_to_english_numerals(arabic_number: str) -> str:
	translation_table = str.maketrans("".join(arabic_numerals),"".join(english_numerals))
	return arabic_number.translate(translation_table)

def filter_result(result:dict):
	for field in ['user_provided_args', 'user_name_length',"name_length","email_ends_with","phone_carrier","phone_start_with","language"]:
		result.pop(field)
	return result

def gender_check(gender):
	assert gender.lower() in genders,"gender must be one of {}".format(genders)

def language_check(language):
	assert language.lower() in languages,"language must be one of {}".format(languages)

def phone_start_with_check(phone_start_with):
	assert phone_start_with.lower() in phone_start_withs,"phone_start_with must be one of {}".format(phone_start_withs)

def phone_carrier_check(phone_carrier):
	assert phone_carrier.lower() in phone_carriers,"phone_carrier must be one of {}".format(phone_carriers)


def email_ends_with_check(email_ends_with):
	assert email_ends_with.lower() in email_ends_withs,"email_ends_with must be one of {}".format(email_ends_withs)

def generate_random_value(values:list,lenght:int=1):
	return "".join([choice(values) for i in range(lenght)])
def generate_name(language:str,gender,name_length):
	language_check(language)
	gender_check(gender)
	if language.lower().startswith('ar'):
		male_names_list = list(male_names.values())
		female_names_list = list(female_names.values())
	else:
		male_names_list = list(male_names.keys())
		female_names_list = list(female_names.keys())
	if gender in male_genders:
		name = choice(male_names_list)
	else:
		name = choice(female_names_list)
	for i in range(name_length-1):
		name += f" {choice(male_names_list)}"
	return name
def generate_city(language:str):
	language_check(language)
	if language.lower().startswith('ar'):
		return choice(list(egyptian_cities.values()))
	else:
		return choice(list(egyptian_cities.keys()))
def generate_job_title(language:str,gender):
	language_check(language)
	gender_check(gender)
	if language.lower().startswith('ar'):
		male_job_tiles = list(male_job_titles.values())
		female_job_tiles = list(female_job_titles.values())

	else:
		male_job_tiles = list(male_job_titles.keys())
		female_job_tiles = list(female_job_titles.keys())
	if gender in male_genders:
		job_title = choice(male_job_tiles)
	else:
		job_title = choice(female_job_tiles)
	return job_title
def generate_phone(language:str,phone_carrier:str,phone_start_with):
	language_check(language)
	from .Randomizer import phone_carriers
	if language.lower().startswith('ar'):
		numerals = arabic_numerals
	else:
		numerals = english_numerals
	if phone_carrier.lower() == 'vodafone':
		phone_perfix = f"{numerals[0]}{numerals[1]}{numerals[0]}"
	elif phone_carrier.lower() == 'etisalat':
		phone_perfix = f"{numerals[0]}{numerals[1]}{numerals[1]}"
	elif phone_carrier.lower() == 'we':
		phone_perfix = f"{numerals[0]}{numerals[1]}{numerals[5]}"
	elif phone_carrier.lower() == 'orange':
		phone_perfix = f"{numerals[0]}{numerals[1]}{numerals[2]}"
	else:
		raise Exception("phone_carrier must be one of {}".format(phone_carriers))
	return f"{phone_start_with}{phone_perfix}" + f"{generate_random_value(numerals,8)}"
def generate_user_name(language:str,user_name_length,name:str):
	language_check(language)
	if language.lower().startswith('ar'):
		numerals = arabic_numerals
	else:
		numerals = english_numerals
	user_name = name.replace(" ","")
	if len(user_name) > user_name_length:
		user_name = user_name[:user_name_length]
	else:
		user_name = f"{user_name}" + generate_random_value(numerals,(user_name_length-len(user_name)))
	return user_name
def generate_national_id(language:str,gender:str,birth_day:int,birth_month:int,birth_year:int):
	language_check(language)
	gender_check(gender)
	if language.lower().startswith('ar'):
		numerals = arabic_numerals
	else:
		numerals = english_numerals
	odd_numerals = [numerals[1], numerals[3], numerals[5], numerals[7], numerals[9]]
	even_numerals = [numerals[0], numerals[2], numerals[4], numerals[6], numerals[8]]
	birth_century = str(birth_year)[:2]
	if language.lower().startswith('ar'):
		birth_century = convert_to_arabic_numerals(birth_century)
	else:
		birth_century = convert_to_english_numerals(birth_century)
	if birth_century == f"{numerals[1]}{numerals[8]}":
		birth_century_value = numerals[1]
	elif birth_century == f"{numerals[1]}{numerals[9]}":
		birth_century_value = numerals[2]
	elif birth_century == f"{numerals[2]}{numerals[0]}":
		birth_century_value = numerals[3]
	else:
		raise Exception("birth_century must be between 18 and 20")
	birth_year = str(birth_year)[2:]
	birth_day = str(birth_day).zfill(2)
	birth_month = str(birth_month).zfill(2)
	if language.lower().startswith('ar'):
		birth_day = convert_to_arabic_numerals(birth_day)
		birth_month = convert_to_arabic_numerals(birth_month)
		birth_year = convert_to_arabic_numerals(birth_year)
	else:
		birth_day = convert_to_english_numerals(birth_day)
		birth_month = convert_to_english_numerals(birth_month)
		birth_year = convert_to_english_numerals(birth_year)
	if gender in male_genders:
		gender_value = f"{choice(odd_numerals)}"
	else:
		gender_value = f"{choice(even_numerals)}"

	return f"{birth_century_value}{birth_year}{birth_month}{birth_day}"+ f"{generate_random_value(numerals,5)}"+f"{gender_value}"
def translate_name(name):
	if name in male_names.keys():
		return male_names[name]
	elif name in female_names.keys():
		return female_names[name]
	elif name in male_names.values():
		return next((k for k, v in male_names.items() if v == name), None)
	elif name in female_names.values():
		return next((k for k, v in female_names.items() if v == name), None)
	else:
		return name
def translate_job_title(job_title):
	if job_title in male_job_titles.keys():
		return male_job_titles[job_title]
	elif job_title in female_job_titles.keys():
		return female_job_titles[job_title]
	elif job_title in male_job_titles.values():
		return next((k for k, v in male_job_titles.items() if v == job_title), None)
	elif job_title in female_job_titles.values():
		return next((k for k, v in female_job_titles.items() if v == job_title), None)
	else:
		return job_title
def translate_city(city):
	if city in egyptian_cities.keys():
		return egyptian_cities[city]
	elif city in egyptian_cities.values():
		return next((k for k, v in egyptian_cities.items() if v == city), None)
	else:
		return city
def translate_number(number):
	number = str(number)
	translated_number = ""
	for n in number:
		if n in arabic_numerals:
			n = english_numerals[arabic_numerals.index(n)]
		elif n in english_numerals:
			n = arabic_numerals[english_numerals.index(n)]
		translated_number += n
	return translated_number
def translate_gender(gender):
	if gender in arabic_genders:
		return english_genders[arabic_genders.index(gender)]
	elif gender in english_genders:
		return arabic_genders[english_genders.index(gender)]
	else:
		return gender
