from pymongo import UpdateOne
from . import Manager
from .myexceptions import AlreadyExistsOnDatabaseException


class UserImageCacheManager(Manager):
    def add(self, username):
        self.newObj = {
            "username": username,
            "images": []
        }
        super().add(username)

    def get(self, username):
        return UserImageCache(username=username, collection=self.collection)


class UserImageCache():

    def __init__(self, username, collection):
        self.username = username
        self.images_cache = collection
        self._user = self.images_cache.find_one({"username": self.username})

    @property
    def images(self):
        return self._user['images']

    def add_images(self, images):
        if type(images) != list:
            images = [images]

        new_images = [image for image in images if image not in self.images]

        if new_images:
            requests = self._add_images(new_images)
            self.images_cache.bulk_write(requests)
        else:
            print('Dont have new images')

    def _add_images(self, new_images):
        requests = []
        for image in new_images:
            requests.append(
                UpdateOne(
                    {'username': self.username},
                    {'$push': {'images': image}}
                )
            )
        return requests

    def remove_image(self, image):
        if not self.isImageExists(image):
            print('Image {} does not exist!'.format(image))
            return

        self.images_cache.find_one_and_update(
            {'username': self.username},
            {'$pull': {
                'images': {
                    '$in': [image]
                }
            }}
        )

    def isImageExists(self, image):
        return image in self.images


class ImageCacheHandler():
    def __init__(self, image_cache_manager):
        self.image_cache_manager = image_cache_manager
        self.image_cache = None

    def get_or_create(self, username):
        try:
            self.image_cache_manager.add(username)
        except AlreadyExistsOnDatabaseException:
            # It is not a problem, go on!
            pass
        finally:
            self.image_cache = self.image_cache_manager.get(username)

    def get_the_news(self, user_images):
        new_images = [
            i for i in user_images
            if not self.image_cache.isImageExists(i)
        ]
        return new_images

    def add_the_images(self, user_images):
        self.image_cache.add_images(user_images)
