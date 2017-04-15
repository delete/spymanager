import telebot
from telebot import types
import logging
from datetime import datetime, timedelta
from decouple import config

from src.messages import *
from src.spy import SpyManager
from src.database import MongoSetup, CollectionFactory
from src.imagesite import ImageSite
from src.subscriptions import SubscriptionsManager
from src.myexceptions import AlreadyExistsOnDatabaseException
from src.imagecache import UserImageCacheManager, ImageCacheHandler
from src.flooder import Flooder
from src.publisher import Publisher

# Read API_KEY from .env file
API_TOKEN = config('API_TOKEN')
ADMIN_ID = config('ADMIN_ID')

bot = telebot.TeleBot(API_TOKEN, threaded=True)

# Database settings
MONGO_URI = 'mongodb://database:27017/data'
DATABASE_NAME = 'spies_database'

mongo_client = MongoSetup(MONGO_URI, DATABASE_NAME)
collection_factory = CollectionFactory(mongo_client)

# Spies collection
spies_collection = collection_factory.create('spies')
spy_manager = SpyManager(spies_collection)

# Subscription collection
subscriptions_collection = collection_factory.create('subscriptions')
subscriptions_manager = SubscriptionsManager(subscriptions_collection)

# Images cache collections
images_cache_collection = collection_factory.create('images_cache')
image_cache_manager = UserImageCacheManager(images_cache_collection)
image_cache_handler = ImageCacheHandler(image_cache_manager)

site = ImageSite()
publisher = Publisher(API_TOKEN)
flood = Flooder(site, publisher, image_cache_handler)


# Time that last advice was posted on group, to avoid spam
last_advice = None


# ##### Helper functios

def isGroup(message):
    return message.chat.type in ["group", "supergroup"]


def destiny(message):
    return message.chat.id


def bot_answer(mensagem, answer, parse_mode='Markdown'):
    chat_id = destiny(mensagem)
    bot.send_message(chat_id, answer, parse_mode)


def nome(message):
    name = message.from_user.first_name
    if not name:
        return message.from_user.username
    return name


def anti_spam_on_group(message):
    global last_advice
    if isGroup(message):
        if not last_advice or datetime.now() - last_advice > timedelta(minutes=15):
            bot_answer(message, BOT_PRIVADO)
            last_advice = datetime.now()
        return True
    else:
        return False


def get_spy(spy_username):
    spy = spy_manager.get(spy_username)
    if spy.exists():
        return spy

    return None


def create_subscriber_from_group(spy_user, group_name):
    return {
        'spy': spy_user.username,
        'group': group_name,
        'chat_id': spy_user.chat_id
    }


def isAllowed(message, spy_user):
    if not spy_user:
        bot_answer(message, REGISTER_FIRST)
        return False
    return True


def isAdmin(message):
    user_id = message.from_user.id
    return int(user_id) == int(ADMIN_ID)


def question(message, question_message, callback):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username
    spy_user = get_spy(username)
    if not isAllowed(message, spy_user):
        return

    markup = types.ForceReply(selective=True)
    replied_message = bot.send_message(
        message.chat.id, question_message, reply_markup=markup
    )

    bot.register_next_step_handler(replied_message, callback)

# ##### Telegram user functions


@bot.message_handler(commands=['whoami'])
def send_whoami(message):
    if anti_spam_on_group(message):
        return
    bot_answer(message, WHOAMI.format(message.from_user))


@bot.message_handler(commands=['register'])
def register_spy(message):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username
    chat_id = message.chat.id
    try:
        spy_manager.add(username, chat_id)
        bot_answer(message, REGISTERED)
    except AlreadyExistsOnDatabaseException:
        bot_answer(message, ALREADY_REGISTER.format(username))


@bot.message_handler(commands=['unregister'])
def unregister_spy(message):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username
    spy_manager.remove(username)

    bot_answer(message, UNREGISTERED)


# ##### Group functions

@bot.message_handler(commands=['addgroup'])
def add_group(message):
    def add_user_to_group(replied_message):
        group_name = replied_message.text.lower()
        spy_user = get_spy(replied_message.from_user.username)

        if not group_name:
            bot_answer(message, 'You forgot the group name!')
            return

        try:
            spy_user.add_group(group_name=group_name)
            bot_answer(replied_message, NEW_GROUP_ADDED.format(group_name))
        except AlreadyExistsOnDatabaseException:
            bot_answer(
                replied_message, 'Group {} already exists!'.format(group_name)
            )

    question_message = "What's the group name?"
    callback = add_user_to_group

    question(message, question_message, callback)


@bot.message_handler(commands=['rmgroup'])
def remove_group(message):
    def _remove_group(replied_message):
        group_name = replied_message.text.lower()
        spy_user = get_spy(replied_message.from_user.username)

        # Must remove all members first, to unsubscriber them
        members_username = spy_user.members_from_group(group_name)

        for member_username in members_username:
            remove_user_from_group(spy_user, member_username, group_name)

        spy_user.remove_group(group_name=group_name)

        bot_answer(message, GROUP_REMOVED.format(group_name))

    question_message = "What's the group name?"
    callback = _remove_group

    question(message, question_message, callback)


@bot.message_handler(commands=['groups'])
def list_groups(message):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username
    spy_user = get_spy(username)
    if not isAllowed(message, spy_user):
        return

    if len(spy_user.groups_names) == 0:
        bot_answer(message, 'There is no group to spy yet!')
        return

    bot_answer(message, 'You are spying these groups:')
    for group in spy_user.groups_names:
        bot_answer(message, group)


@bot.message_handler(commands=['groupusers'])
def list_group_members(message):
    def members_from_group(replied_message):
        group_name = replied_message.text.lower()
        spy_user = get_spy(replied_message.from_user.username)

        if not group_name:
            bot_answer(message, 'You forgot the group name!')
            return

        members_username = spy_user.members_from_group(group_name=group_name)
        bot_answer(message, 'Users from {} group:'.format(group_name))
        for member in members_username:
            bot_answer(message, member)

    question_message = "What's the group name?"
    callback = members_from_group

    question(message, question_message, callback)


@bot.message_handler(commands=['updategroup'])
def list_groups_to_update_images(message):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username
    spy_user = get_spy(username)
    if not isAllowed(message, spy_user):
        return

    markup = types.ReplyKeyboardMarkup(row_width=4, one_time_keyboard=True)

    groups_names = []

    if len(spy_user.groups_names) == 0:
        bot_answer(message, 'There is no group created yet!')
        return

    for group in spy_user.groups_names:
        groups_names.append(types.KeyboardButton('${}'.format(group)))

    markup.add(*groups_names)
    chat_id = destiny(message)
    bot.send_message(chat_id, REGISTERED_GROUPS, reply_markup=markup)


@bot.message_handler(regexp="^\$.*")
def update_images_from_group(message):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username
    spy_user = get_spy(username)
    if not isAllowed(message, spy_user):
        return

    who = 'spy'
    if isAdmin(message):
        who = 'boss'

    group_name = message.text.split('$')[1]

    bot_answer(
        message, 'Wait a minute {}... this can take some time.'.format(who)
    )

    subscriptions = subscriptions_manager.filterByGroup(spy_user, group_name)
    flood.flood_to(subscriptions)

    bot_answer(message, 'Everything was sent {}!'.format(who))


# ##### Users functions
group_name = ''


@bot.message_handler(commands=['adduser'])
def add_user(message):
    def add_users_to_group(replied_message):
        members_usernames = replied_message.text.split(',')
        spy_user = get_spy(replied_message.from_user.username)

        spy_user.add_members_to_group(
            members_username=members_usernames, group_name=group_name
        )

        subscriber = create_subscriber_from_group(spy_user, group_name)

        for member in members_usernames:
            try:
                subscriptions_manager.add(member)
            except AlreadyExistsOnDatabaseException:
                continue

        for member in members_usernames:
            s = subscriptions_manager.get(member)
            s.add_subscribers(subscriber)

        if members_usernames:
            bot_answer(
                message,
                NEW_USER_ADDED_TO_GROUP.format(
                    ' @'.join(members_usernames),
                    group_name
                )
            )

    def get_group_name(replied_message):
        global group_name
        group_name = replied_message.text.lower()

        question_message = "Who do you wanna spy on?"
        callback = add_users_to_group

        question(message, question_message, callback)

    question_message = "What's the GROUP name?"
    callback = get_group_name

    question(message, question_message, callback)


@bot.message_handler(commands=['rmuser'])
def remove_user(message):
    def _remove_user(replied_message):
        member_username = replied_message.text.split(',')
        spy_user = get_spy(replied_message.from_user.username)

        remove_user_from_group(spy_user, member_username, group_name)

        bot_answer(
            message,
            USER_REMOVED_FROM_GROUP.format(member_username, group_name)
        )

    def get_group_name(replied_message):
        global group_name
        group_name = replied_message.text.lower()

        question_message = "Who do you wanna remove?"
        callback = _remove_user

        question(message, question_message, callback)

    question_message = "What's the GROUP name?"
    callback = get_group_name

    question(message, question_message, callback)


def remove_user_from_group(spy_user, member_username, group_name):
    spy_user.remove_member_from_group(
        member_username=member_username, group_name=group_name
    )

    subscriber = create_subscriber_from_group(spy_user, group_name)

    s = subscriptions_manager.get(member_username)
    s.remove_subscriber(subscriber)

    # Must remove the subscription, to do not get his images any longer
    if not s.subscribers:
        subscriptions_manager.remove(member_username)


# ##### Send functions

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if anti_spam_on_group(message):
        return
    bot_answer(message, ABOUT.format(nome(message)))

    username = message.from_user.username
    spy_user = get_spy(username)

    if spy_user:
        bot_answer(message, ALREADY_REGISTER.format(username))


@bot.message_handler(commands=['help', 'ajuda'])
def send_help(message):
    if anti_spam_on_group(message):
        return
    bot_answer(message, HELP)


@bot.message_handler(commands=['link', 'links'])
def send_link(message):
    if anti_spam_on_group(message):
        return
    bot_answer(message, LINKS)


@bot.message_handler(commands=['updateall'])
def update_all_images(message):
    if anti_spam_on_group(message):
        return

    if not isAdmin(message):
        bot_answer(message, 'You are not the big boss!')
        return

    bot_answer(message, 'Wait a minute boss... this can take some time.')

    subscriptions = subscriptions_manager.all()
    flood.flood_to(subscriptions)

    bot_answer(message, 'Everything was sent boss!')


@bot.message_handler(regexp="^\@.*")
def send_user_photos(message):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username
    spy_user = get_spy(username)
    if not isAllowed(message, spy_user):
        return

    username = message.text.split('@')[1]

    image_site = ImageSite()
    user = image_site.get_user(username)

    for image in user.images:
        bot_answer(message, image)


_logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot.polling(none_stop=True)
