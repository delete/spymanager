import pymongo


class MongoSetup():
    def __init__(self, uri, databaseName):
        self.uri = uri
        self.databaseName = databaseName
        self._create_client()

    def use_collection(self, collectionName):
        self.collection = self._db.get_collection(name=collectionName)

    def _create_client(self):
        self.client = pymongo.MongoClient(self.uri)
        self._db = self.client[self.databaseName]

    def create_index(self, field, unique=True):
        self.collection.create_index(
            [(field, pymongo.ASCENDING)], unique=unique
        )


class CollectionFactory():
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client

    def create(self, collectionName, index=True):
        self.mongo_client.use_collection(collectionName)
        if index:
            self.mongo_client.create_index(field='username')

        return self.mongo_client.collection
