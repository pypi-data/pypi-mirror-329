import unittest
#from faker import Faker
class Faker:
	pass
fake = Faker()

def generate_person():
    """Generates a random person's information."""
    return {
        "name": fake.name(),
        "address": fake.address(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
        "ssn": fake.ssn()
    }
class TestGenerator(unittest.TestCase):
    def test_generate_person(self):
        person = generate_person()
        self.assertIn("name", person)
        self.assertIn("email", person)
        self.assertTrue(person["name"])
        self.assertTrue(person["email"])

if __name__ == "__main__":
    unittest.main()
