from src.imagesite import ImageSite

from src.group import Group

image_site = ImageSite()

developers = Group('developers')

usernames = ['pinheirofellipe', 'mazulo_']

for username in usernames:
    user = image_site.get_user(username)
    developers.add_user(user)

developers.get_images()
