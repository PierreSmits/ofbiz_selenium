from faker import Faker
import random

class UserFactory:
    def __init__(self):
        self.factory = []
        self.factorySize = 0

    def generate(self):
        user = Faker()
        first = user.first_name()
        last = user.last_name()
        address = user.address()
        city = user.city()
        postal = user.zipcode()
        email = user.email()
        login = first.lower() + "_" + last.lower()
        passwd = user.password()
        confirm = passwd
        
        credentials = (first, last, address, city, postal, email, login, passwd, confirm)
        self.factory.append(credentials)
        self.factorySize = self.factorySize + 1
        return credentials

    def getRandomCredentials(self, type='login'):
        userId = random.choice(range(self.factorySize))
        credentials = self.factory[userId]

        if type=="account":
            return credentials

        name = credentials[0] + " " + credentials[1]
        user = credentials[6]
        passwd = credentials[7]
        return (user, passwd, name)
