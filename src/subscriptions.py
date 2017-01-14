from pymongo.errors import BulkWriteError
from . import Manager


class SubscriptionsManager(Manager):
    def add(self, username):
        self.newObj = {
            "username": username,
            "subscribers": []
        }
        super().add(username)

    def get(self, username):
        return Subscription(username=username, collection=self.collection)


class Subscription():

    def __init__(self, username, collection):
        self.username = username
        self.subscriptions = collection

        self.bulk = self.subscriptions.initialize_unordered_bulk_op()

    @property
    def _user(self):
        return self.subscriptions.find_one({"username": self.username})

    @property
    def subscribers(self):
        return self._user['subscribers']

    def exists(self):
        return self._user is not None

    def add_subscribers(self, subscribers):
        for subscriber in subscribers:
            if not self._is_subscriber_exists(subscriber):
                self.bulk.find(
                    {'username': self.username}
                ).update({'$push': {'subscribers': subscriber}})

            else:
                msg = 'Subscriber {} already exists with group {}!'
                print(msg.format(subscriber['spy'], subscriber['group']))
        try:
            self.bulk.execute()
        except BulkWriteError as bwe:
            print(bwe.details)

    def remove_subscriber(self, subscriber):
        if not self._is_subscriber_exists(subscriber):
            msg = 'Subscriber {} with group {} does not exist!'
            print(msg.format(subscriber['spy'], subscriber['group']))
            return

        self.subscriptions.find_one_and_update(
            {'$and': [
                {'username': self.username},
                {'subscribers.spy': subscriber['spy']},
                {'subscribers.group': subscriber['group']}
            ]},
            {'$pull': {'subscribers': {'$in': [subscriber]}}}
        )

    def _is_subscriber_exists(self, subscriber_find):
        subscriber = self.subscriptions.find_one(
            {'$and': [
                {'username': self.username},
                {'subscribers.spy': subscriber_find['spy']},
                {'subscribers.group': subscriber_find['group']}
            ]})

        return subscriber is not None
