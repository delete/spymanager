from src.database import MongoSetup

MONGO_URI = 'mongodb://localhost:27017/data'


# Database settings
def create_database_connection(database_name, collection_name):
    mongo = MongoSetup(MONGO_URI, database_name, collection_name)
    mongo.create_index(field='username')
    # Clear the collection before start the test
    mongo.collection.drop()

    return mongo
