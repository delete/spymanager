import sys
sys.path.insert(0, '../spymanager')
sys.path.insert(0, '../')

from tests import create_database_connection
from src.subscriptions import SubscriptionsManager


# Database settings
DATABASE_NAME = 'spies_database'
COLLECTION_NAME = 'subscriptions'
mongo = create_database_connection(DATABASE_NAME, COLLECTION_NAME)

subscriptions_manager = SubscriptionsManager(mongo)

# User to test
USERNAME = 'pinheirofellipe'

# Clear before tests
subscriptions_manager.remove(USERNAME)

subscriptions_manager.add(USERNAME)

user = subscriptions_manager.get(USERNAME)

assert user.username == USERNAME

assert user.exists() is True

subscribers = [
    {
        "spy": "spy1",
        "group": "g1"
    }, {
        "spy": "spy2",
        "group": "g1"
    }
]

user.add_subscribers(subscribers)

assert len(user.subscribers) == 2

subscriber_to_remove = {
    "spy": "spy1",
    "group": "g1"
}

user.remove_subscriber(subscriber_to_remove)

assert len(user.subscribers) == 1

print('Well done!')
