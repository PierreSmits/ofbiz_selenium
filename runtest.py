from ofbiztest import OfbizTest
from userfactory import UserFactory
import random
import time
import sys

if __name__ == '__main__':
    test = OfbizTest()
    users = UserFactory()
    keywords = ["asum", "bpm", "rca", "platform"]
    userCount = int(sys.argv[1])

    for i in range(userCount):
        loops = random.choice(range(1, 4))
        test.go()
        test.createAccount(users.generate())
        test.buyProducts(keywords, loops)
        test.reset()

    for i in range(2*userCount):
        loops = random.choice(range(1, 5))
        test.go()
        test.login(users.getRandomCredentials())
        try:
            test.buyProducts(keywords, loops)
        except:
            pass
        test.reset()

    test.finish()