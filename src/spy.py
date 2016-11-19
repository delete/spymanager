from src.myexceptions import GroupNotFoundException
from src.group import Group


class Spy():
    """ User bot model """

    def __init__(self, username, groups=[]):
        self.username = username
        self.groups = groups

    def __repr__(self):
        return '{}'.format(self.username)

    def add_group(self, groupname):
        group = self.find_group(groupname)
        if group is None:
            newgroup = Group(name=groupname)
            self.groups.append(newgroup)

    def rm_group(self, groupname):
        group = self.find_group(groupname)
        if group is None:
            raise GroupNotFoundException

        self.groups.remove(group)

    def add_user_to_group(self, username, groupname):
        group = self.find_group(groupname)
        if group is None:
            raise GroupNotFoundException
        group.add_user(username)

    # Return the group object by given the group name
    def find_group(self, groupname):
        for group in self.groups:
            if group.name == groupname:
                return group
        return None

    def clear(self):
        for group in self.groups:
            group.clear()
        self.groups = []
