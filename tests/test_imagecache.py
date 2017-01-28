import sys
sys.path.insert(0, '../spymanager')
sys.path.insert(0, '../')

from tests import create_database_connection
from src.imagecache import UserImageCacheManager


# Database settings
DATABASE_NAME = 'spies_database'
COLLECTION_NAME = 'images_cache'
mongo = create_database_connection(DATABASE_NAME, COLLECTION_NAME)

# User to test
USERNAME = 'pinheirofellipe'

user_image_manager = UserImageCacheManager(mongo)

# Clear before tests
user_image_manager.remove(USERNAME)

user_image_manager.add(USERNAME)

all_user_images = user_image_manager.all()

assert len(all_user_images) == 1

user = user_image_manager.get(USERNAME)

assert user.username == USERNAME

images = [
    'someURL1', 'someURL2', 'someURL3'
]

user.add_images(images)

assert len(user.images) == 3

image_to_remove = 'someURL1'

user.remove_image(image_to_remove)

assert len(user.images) == 2

print('Well done!')
