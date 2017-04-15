import pymongo
from .myexceptions import AlreadyExistsOnDatabaseException

TELEGRAM_URL = 'https://api.telegram.org/bot{token}/{method}?chat_id={chat_id}&text={text}'


class Manager():
    """ Manage objects adding, removing and getting from database """

    def __init__(self, collection):
        self.collection = collection

    def add(self, username):
        try:
            self.collection.insert_one(self.newObj)
        except pymongo.errors.DuplicateKeyError:
            raise AlreadyExistsOnDatabaseException

    def remove(self, username):
        self.collection.find_one_and_delete({"username": username})

    def all(self):
        cursor = self.collection.find()
        return [document for document in cursor]

    def get(self, username):
        pass
