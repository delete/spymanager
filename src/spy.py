import datetime
import pymongo


class SpyManager():
    def __init__(self, database):
        self.database = database

        self.spies = self.database.collection

    def add_spy(self, username):
        newSpy = {
            "username": username,
            "groups": [],
            "created": datetime.datetime.utcnow()
        }

        try:
            self.spies.insert_one(newSpy)
        except pymongo.errors.DuplicateKeyError:
            print('Spy {} already exists!'.format(newSpy['username']))

    def remove_spy(self, username):
        self.spies.find_one_and_delete({"username": username})

    def get_spy(self, username):
        return Spy(username=username, collection=self.spies)


class Spy():
    """ Spy model that wrapper spy mongo object"""

    def __init__(self, username, collection):
        self.username = username
        self.spies = collection

    @property
    def _spy(self):
        return self.spies.find_one({"username": self.username})

    @property
    def groups(self):
        return self._spy['groups']

    @property
    def groups_names(self):
        return [group['name'] for group in self.groups]

    def members_from_group(self, group_name):
        found_group = None
        for group in self.groups:
            if group['name'] == group_name:
                found_group = group
                break
        return found_group['users']

    def exists(self):
        return self._spy is not None

    def add_group(self, group_name):
        newGroup = {
            "name": group_name,
            "users": []
        }

        if newGroup['name'] not in self.groups_names:
            self.spies.find_one_and_update(
                {'username': self.username},
                {'$push': {'groups': newGroup}}
            )
        else:
            print('Group {} already exists!'.format(newGroup['name']))

    def remove_group(self, group_name):
        if not self._isGroupExists(group_name):
            print('Group {} does not exist!'.format(group_name))
            return

        self.spies.find_one_and_update(
            {'$and': [
                {'username': self.username},
                {'groups.name': group_name}
            ]},
            {'$pull': {'groups': {"name": group_name}}}
        )

    def add_member_to_group(self, member_username, group_name):
        found_group = None

        for group in self.groups:
            if group['name'] == group_name:
                found_group = group
                break

        if found_group:
            if member_username not in found_group['users']:
                self.spies.find_one_and_update(
                    {'$and': [
                        {'username': self.username},
                        {'groups.name': group_name}
                    ]},
                    {'$push': {'groups.$.users': member_username}}
                )
        else:
            print('Group {} does not exist!'.format(group_name))

    def remove_member_from_group(self, member_username, group_name):
        if not self._isGroupExists(group_name):
            print('Group {} does not exist!'.format(group_name))
            return

        self.spies.find_one_and_update(
            {'$and': [
                {'username': self.username},
                {'groups.name': group_name}
            ]},
            {'$pull': {'groups.$.users': {'$in': [member_username]}}}
        )

    def _isGroupExists(self, group_name):
        return group_name in self.groups_names
