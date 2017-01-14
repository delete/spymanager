import pymongo
from .myexceptions import AlreadyExistsOnDatabaseException


class Manager():
    """ Manage objects adding, removing and getting from database """

    def __init__(self, database):
        self.database = database
        self.collection = self.database.collection

    def add(self, username):
        try:
            self.collection.insert_one(self.newObj)
        except pymongo.errors.DuplicateKeyError:
            raise AlreadyExistsOnDatabaseException

    def remove(self, username):
        self.collection.find_one_and_delete({"username": username})

    def get(self, username):
        pass