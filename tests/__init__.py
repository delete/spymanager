from src.database import MongoSetup, CollectionFactory

MONGO_URI = 'mongodb://localhost:27017/data'


# Database settings
def create_database_collection(database_name, collection_name):
    mongo_client = MongoSetup(MONGO_URI, database_name)
    collection_factory = CollectionFactory(mongo_client)
    collection = collection_factory.create(collection_name)
    # Clear the collection before start the test
    collection.drop()

    return collection
