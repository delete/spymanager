from pymongo.errors import BulkWriteError
from . import Manager


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

        self.bulk = self.images_cache.initialize_unordered_bulk_op()

    @property
    def _user(self):
        return self.images_cache.find_one({"username": self.username})

    @property
    def images(self):
        return self._user['images']

    def exists(self):
        return self._user is not None

    def add_images(self, images):
        new_images = []

        if type(images) != list:
            images = [images]

        for image in images:
            if image not in self.images:
                new_images.append(image)

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
        if not self._isImageExists(image):
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

    def _isImageExists(self, image):
        return image in self.images
