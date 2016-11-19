from src.myexceptions import UserNotFoundException
from src.imagesite import ImageSite


class Group():
    """ SiteImage users' group model """

    def __init__(self, name, users=[], site=None):
        self.name = name
        self.users = users

        self._site = site
        # Set default site
        if not self._site:
            self._site = ImageSite()

    def __repr__(self):
        return '{}'.format(self.name)

    def add_user(self, username):
        user = self._find_user(username)
        if user is None:
            user = self._site.get_user(username)
            self.users.append(user)

    def rm_user(self, username):
        user = self._find_user(username)
        if user is None:
            raise UserNotFoundException

        self.users.remove(user)

    def _find_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def clear(self):
        self.users = []
