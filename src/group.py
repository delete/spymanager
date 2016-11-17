
class Group():
    """ SiteImage users' group model """

    def __init__(self, name, users=[]):
        self.name = name
        self.users = users

    def __repr__(self):
        return '{}'.format(self.name)

    def add_user(self, user):
        self.users.append(user)

    def clear(self):
        self.users = []

    def get_images(self):
        for user in self.users:
            user.pretty_print()
