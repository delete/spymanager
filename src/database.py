import pymongo


class MongoSetup():
    def __init__(self, uri, databaseName, collectionName):
        self.uri = uri
        self.databaseName = databaseName
        self.collectionName = collectionName

        self._create_client()
        self._db = self.client.databaseName
        self.collection = self._db.collectionName

    def _create_client(self):
        self.client = pymongo.MongoClient(self.uri)

    def create_index(self, field, unique=True):
        self.collection.create_index(
            [(field, pymongo.ASCENDING)], unique=unique
        )
