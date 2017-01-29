from pymongo.errors import BulkWriteError
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

        self.bulk = self.images_cache.initialize_ordered_bulk_op()

    @property
    def _user(self):
        return self.images_cache.find_one({"username": self.username})

    @property
    def images(self):
        return self._user['images']

    def add_images(self, images):
        if type(images) != list:
            images = [images]

        new_images = [image for image in images if image not in self.images]

        if new_images:
            for image in new_images:
                self.bulk.find(
                    {'username': self.username}
                ).update({'$push': {'images': image}})

            try:
                self.bulk.execute()
            except BulkWriteError as bwe:
                print(bwe.details)
        else:
            print('Dont have new images')

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
