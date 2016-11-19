from src.spy import Spy

# Adding bot user
spy_user = Spy(username='delete')

# Adding some groups
spy_user.add_group(groupname='devs')
spy_user.add_group(groupname='sports')

# Adding some users to 'devs' group
spy_user.add_user_to_group(username='pinheirofellipe', groupname='devs')
spy_user.add_user_to_group(username='mazulo_', groupname='devs')

print("My groups: {}".format(spy_user.groups))

# Get group object
devs = spy_user.find_group('devs')

print("'devs' group users: {}".format(devs.users))


print("\n######################")
print("'devs' group images")
print("######################\n")

for user in devs.users:
    print("{} images \n\n".format(user))

    for imagecode in user.images:
        print(user.images[imagecode]['src'])

    print("######################\n")
