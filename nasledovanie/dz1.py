class User:
    def __init__(self, name):
        self.name = name

    def skip_ads(self):
        return False


class PremiumUser(User):
    def skip_ads(self):
        return True

user = User("Alex")
premium = PremiumUser("John")

print(user.name, user.skip_ads())
print(premium.name, premium.skip_ads())