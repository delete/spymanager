import datetime
# import pymongo
from pymongo.errors import BulkWriteError
from . import Manager


class SpyManager(Manager):
    def add(self, username):
        self.newObj = {
            "username": username,
            "groups": [],
            "created": datetime.datetime.utcnow()
        }
        super().add(username)

    def get(self, username):
        return Spy(username=username, collection=self.collection)


class Spy():
    """ Spy model that wrappers spy mongo object """

    def __init__(self, username, collection):
        self.username = username
        self.spies = collection

        self.bulk = self.spies.initialize_unordered_bulk_op()

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

    def add_members_to_group(self, members_username, group_name):
        found_group = None

        if type(members_username) != list:
            members_username = [members_username]

        for group in self.groups:
            if group['name'] == group_name:
                found_group = group
                break

        if found_group:
            new_members = [
                member for member in members_username
                if member not in found_group['users']
            ]
            for member in new_members:
                self.bulk.find({'$and': [
                    {'username': self.username},
                    {'groups.name': group_name}
                ]}).update({'$push': {'groups.$.users': member}})

            try:
                self.bulk.execute()
            except BulkWriteError as bwe:
                print(bwe.details)
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
