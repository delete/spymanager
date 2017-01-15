import gevent
from gevent import monkey, pool


monkey.patch_all()


class Flooder():
    def __init__(self, site, publisher, image_cache_handler):
        self.site = site
        self.publisher = publisher
        self.image_cache_handler = image_cache_handler

        self.cache_handlers = []

    def _push_to(self, chat_id, messages):
        self.publisher.send_to(chat_id)
        for message in messages:
            self.publisher.send(message)

    def _pull_from(self, subscription):
        user = self.site.get_user(subscription['username'])

        self.image_cache_handler.get_or_create(username=user.username)
        new_images = self.image_cache_handler.get_the_news(user.images)

        # This need run after send all images, because bulk is raising an
        # InvalidOperation Exception: Bulk operations can only be executed once
        self.image_cache_handler.add_the_images(new_images)

        chat_ids = [s['chat_id'] for s in subscription['subscribers']]

        p = pool.Pool(5)
        for _id in chat_ids:
            p.spawn(self._push_to, _id, new_images)
        p.join()

    def flood_to(self, subscriptions):
        jobs = [
            gevent.spawn(self._pull_from, subscription)
            for subscription in subscriptions
        ]
        gevent.wait(jobs)
