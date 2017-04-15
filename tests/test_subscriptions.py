import sys
sys.path.insert(0, '../spymanager')
sys.path.insert(0, '../')

from tests import create_database_collection
from src.subscriptions import SubscriptionsManager


# Database settings
DATABASE_NAME = 'spies_database'
COLLECTION_NAME = 'subscriptions'
subscriptions_collection = create_database_collection(DATABASE_NAME, COLLECTION_NAME)

subscriptions_manager = SubscriptionsManager(subscriptions_collection)

# User to test
USERNAME = 'pinheirofellipe'

# Clear before tests
subscriptions_manager.remove(USERNAME)

subscriptions_manager.add(USERNAME)

all_subscritions = subscriptions_manager.all()

assert len(all_subscritions) == 1

user = subscriptions_manager.get(USERNAME)

assert user.username == USERNAME

assert user.exists() is True

subscribers = [
    {
        "spy": "spy1",
        "group": "g1",
        "chat_id": 123456
    }, {
        "spy": "spy2",
        "group": "g1",
        "chat_id": 654321
    }
]

user.add_subscribers(subscribers)

assert len(user.subscribers) == 2

subscriber_to_remove = {
    "spy": "spy1",
    "group": "g1",
    "chat_id": 123456
}

user.remove_subscriber(subscriber_to_remove)

assert len(user.subscribers) == 1

print('Well done!')
