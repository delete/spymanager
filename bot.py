import telebot
from telebot import types
import logging
from datetime import datetime, timedelta

from src.messages import *
from src.spy import SpyManager
from src.database import MongoSetup
from src.imagesite import ImageSite


with open('.env') as file:
    API_TOKEN = file.read()

assert API_TOKEN is not None

bot = telebot.TeleBot(API_TOKEN, threaded=True)


# Database settings
MONGO_URI = 'mongodb://database:27017/data'
DATABASE_NAME = 'spies_database'
COLLECTION_NAME = 'spies'

mongo = MongoSetup(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)
mongo.create_index(field='username')

spy_manager = SpyManager(mongo)


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


def registered_spy(spy_username):
    spy = spy_manager.get_spy(spy_username)
    if spy.exists():
        return spy

    return None


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
    spy_manager.add_spy(username)

    bot_answer(message, REGISTERED)


@bot.message_handler(commands=['unregister'])
def unregister_spy(message):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username
    spy_manager.remove_spy(username)

    bot_answer(message, UNREGISTERED)


# ##### Group functions

@bot.message_handler(commands=['addgroup'])
def add_group(message):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username

    spy_user = registered_spy(username)

    if not spy_user:
        bot_answer(message, REGISTER_FIRST)

    params = message.text.split()

    if len(params) < 2:
        bot_answer(message, 'You forgot the group name!')

    spy_user.add_group(group_name=params[1])

    bot_answer(message, NEW_GROUP_ADDED.format(params[1]))


@bot.message_handler(commands=['rmgroup'])
def remove_group(message):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username

    spy_user = registered_spy(username)

    if not spy_user:
        bot_answer(message, REGISTER_FIRST)

    params = message.text.split()

    if len(params) < 2:
        bot_answer(message, 'You forgot the group name!')

    spy_user.remove_group(group_name=params[1])

    bot_answer(message, GROUP_REMOVED.format(params[1]))


@bot.message_handler(commands=['groups'])
def list_groups(message):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username

    spy_user = registered_spy(username)

    if not spy_user:
        bot_answer(message, REGISTER_FIRST)

    markup = types.ReplyKeyboardMarkup(row_width=4, one_time_keyboard=True)

    groups_names = []

    if len(spy_user.groups_names) == 0:
        bot_answer(message, 'There is no group created yet!')
        return

    for group in spy_user.groups_names:
        groups_names.append(types.KeyboardButton('${}'.format(group)))

    if len(groups_names) == 0:
        bot_answer(message, 'No group created!')

    markup.add(*groups_names)
    chat_id = destiny(message)
    bot.send_message(chat_id, REGISTERED_GROUPS, reply_markup=markup)


@bot.message_handler(regexp="^\$.*")
def members_from_group(message):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username

    spy_user = registered_spy(username)

    if not spy_user:
        bot_answer(message, REGISTER_FIRST)

    markup = types.ReplyKeyboardMarkup(row_width=4, one_time_keyboard=True)

    group_name = message.text.split('$')[1]

    members = spy_user.members_from_group(group_name)

    members_names = []
    for member in members:
            members_names.append(types.KeyboardButton('@{}'.format(member)))

    if len(members_names) == 0:
        bot_answer(message, 'No members at this group!')

    markup.add(*members_names)
    chat_id = destiny(message)
    bot.send_message(
        chat_id, MEMBERS_GROUPS.format(group_name), reply_markup=markup
    )


# ##### Users functions

@bot.message_handler(commands=['adduser'])
def add_user(message):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username

    spy_user = registered_spy(username)

    if not spy_user:
        bot_answer(message, REGISTER_FIRST)

    params = message.text.split()

    if len(params) < 3:
        bot_answer(message, 'You forgot some params!')

    spy_user.add_member_to_group(
        member_username=params[1], group_name=params[2]
    )

    bot_answer(message, NEW_USER_ADDED_TO_GROUP.format(params[1], params[2]))


@bot.message_handler(commands=['rmuser'])
def remove_user(message):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username

    spy_user = registered_spy(username)

    if not spy_user:
        bot_answer(message, REGISTER_FIRST)

    params = message.text.split()

    if len(params) < 3:
        bot_answer(message, 'You forgot some params!')

    spy_user.remove_member_from_group(
        member_username=params[1], group_name=params[2]
    )

    bot_answer(message, USER_REMOVED_FROM_GROUP.format(params[1], params[2]))


# ##### Send functions

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if anti_spam_on_group(message):
        return
    bot_answer(message, ABOUT.format(nome(message)))

    username = message.from_user.username

    spy_user = registered_spy(username)

    if spy_user:
        bot_answer(message, ALREADY_REGISTER.format(username))


@bot.message_handler(commands=['help', 'ajuda'])
def send_help(message):
    if anti_spam_on_group(message):
        return
    bot_answer(message, AJUDA)


@bot.message_handler(commands=['link', 'links'])
def send_link(message):
    if anti_spam_on_group(message):
        return
    bot_answer(message, LINKS)


@bot.message_handler(regexp="^\@.*")
def send_user_photos(message):
    if anti_spam_on_group(message):
        return

    username = message.from_user.username

    spy_user = registered_spy(username)

    if not spy_user:
        bot_answer(message, REGISTER_FIRST)

    username = message.text.split('@')[1]

    image_site = ImageSite()
    user = image_site.get_user(username)

    for image in user.images:
        bot_answer(message, user.images[image]['src'])


_logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot.polling(none_stop=True)
