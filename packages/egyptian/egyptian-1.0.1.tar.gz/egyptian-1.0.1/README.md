[![PyPI Downloads](https://static.pepy.tech/badge/egyptian)](https://pepy.tech/projects/egyptian)[![PyPI Downloads](https://static.pepy.tech/badge/egyptian/month)](https://pepy.tech/projects/egyptian)[![PyPI Downloads](https://static.pepy.tech/badge/egyptian/week)](https://pepy.tech/projects/egyptian)
# Egyptian
Generate Random Egyptian Information

## Installation
```bash
pip install egyptian
```
## Update
```bash
pip install --upgrade egyptian
```

## Usage
### Generate Random Egyptian Information
#### for one person
```python
from egyptian import Person

person = Person()
print(person.get_all())
```
#### with specific number of people
```python
from egyptian import Person

person = Person()
print(person.get_all(10))
```
#### with specific arguments:
- language:str(optional):options = ['ar', 'en',"arabic","english"]
```python    
from egyptian import Person

person = Person(language="en")
print(person.get_all())
```
- gender:str(optional):options = ['ذكر', 'male','أنثي', 'female']
```python    
from egyptian import Person

person = Person(gender="male")
print(person.get_all())
```
- name_length:int(optional)
```python    
from egyptian import Person

person = Person(name_length=10)
print(person.get_all())
```
- age:int(optional)
```python    
from egyptian import Person

person = Person(age=20)
print(person.get_all())
```
- name:str(optional)
```python    
from egyptian import Person

person = Person(name="Ali")
print(person.get_all())
```
- city:str(optional)
```python    
from egyptian import Person

person = Person(city="Cairo")
print(person.get_all())
```
- job_title:str(optional)
```python    
from egyptian import Person

person = Person(job_title="Engineer")
print(person.get_all())
```
- phone_carrier:str(optional)['orange', 'we', 'vodafone',"etisalat"]
```python    
from egyptian import Person

person = Person(phone_carrier="Vodafone")
print(person.get_all())
```
- phone_start_with:str(optional)['2', '+2','٢',"+٢",""]
```python    
from egyptian import Person 

person = Person(phone_start_with="010")
print(person.get_all())
```
- phone:str(optional)
```python    
from egyptian import Person

person = Person(phone="0123456789")
print(person.get_all())
```
- user_name_length:int(optional)
```python    
from egyptian import Person

person = Person(user_name_lenght=10)
print(person.get_all())
```
- user_name:str(optional)
```python    
from egyptian import Person

person = Person(user_name="ali1234")
print(person.get_all())
```
- email_ends_with:str(optional)['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'aol.com', 'icloud.com', 'protonmail.com', 'zoho.com', 'gmx.com', 'yandex.com']
```python    
from egyptian import Person 

person = Person(email_ends_with="gmail.com")
print(person.get_all())
```
- email:str(optional)
```python    
from egyptian import Person

person = Person(email="b9Kb3@example.com")
print(person.get_all())
```
- national_id:str(optional)
```python    
from egyptian import Person

person = Person(national_id="123456789101112")    
print(person.get_all())
```
### Update Egyptian Information
- Randomly
```python
from egyptian import Person
person = Person()
print(person.get_all())
person.update_name()
person.update_job_title()
person.update_city()
person.update_national_id()
person.update_phone()
person.update_user_name()
print(person.get_all())
```
- with specific arguments:
```python
from egyptian import Person
person = Person()
print(person.get_all())
person.update_name(gender="female",name_length=10,language="ar")
person.update_job_title(language="en",gender="female")
person.update_city(language="ar") 
person.update_national_id(language="en",birth_day=1,birth_month=1,birth_year=2000)
person.update_phone(language="en",phone_carrier="Vodafone",phone_start_with="+2")
person.update_user_name(language="en",user_name_lenght=10)
print(person.get_all())
```
### Translate Egyptian Information
```python
from egyptian import Person
person = Person()
print(person.get_all())
person.translate_name()
person.translate_job_title()
person.translate_city()
person.translate_national_id()
person.translate_phone()
person.translate_user_name()
print(person.get_all())
```

## Features
- Generate random Egyptian names (male/female)
- Generate phone numbers with Egyptian carriers
- Generate realistic national IDs
- Convert numbers between Arabic and English formats
- Translate between Arabic and English for names, cities, and job titles

## License
MIT License
