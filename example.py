from src.database import MongoSetup
from src.spy import SpyManager
from src.imagesite import ImageSite


# Database settings
MONGO_URI = 'mongodb://database:27017/data'
DATABASE_NAME = 'spies_database'
COLLECTION_NAME = 'spies'

# User to test
USERNAME = 'pinheirofellipe'

mongo = MongoSetup(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)
mongo.create_index(field='username')

# Spy actions
spy_manager = SpyManager(mongo)

# Remove if it's exists
spy_manager.remove_spy(USERNAME)

# Adding bot user
spy_manager.add_spy(USERNAME)

# Get created spy
spy = spy_manager.get_spy(USERNAME)

# Adding groups
new_group = 'devs'
spy.add_group(new_group)

new_group = 'sports'
spy.add_group(new_group)

# Adding user to group
member_mazulo = 'mazulo_'
member_pinheiro = 'pinheirofellipe'
group_to_add = 'devs'

spy.add_members_to_group([member_mazulo, member_pinheiro], group_to_add)

# Remove group
spy.remove_group('sports')

# Printing
print('\nMy groups: {}'.format(spy.groups))

# Removing member
print("\n Removing mazulo_ from devs")
spy.remove_member_from_group('mazulo_', 'devs')

print('\nMy groups: {}'.format(spy.groups))

site = ImageSite()

for group in spy.groups:
    print('\n\n\t\tMembers from {} group\n\n'.format(group['name']))

    for member_username in group['users']:
        print('\n\tImages from {}\n\n'.format(member_username))
        user = site.get_user(member_username)
        user.print_images_urls()
