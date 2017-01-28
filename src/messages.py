WHOAMI = """
User: @{0.username}
ID: {0.id}
Name: {0.first_name} {0.last_name}
"""

REGISTER_FIRST = """
To initiate, register first!

/register
"""

ALREADY_REGISTER = """
I can see that you're already register {0}.

Type /help and enjoy!
"""
REGISTERED = """
You was registered.

Now you can create a group and add some users to it.
"""

ABOUT = """
Hi {0}, I'm Spies Manager Bot and I can help you to be a spy too!

With me you can create groups and add users, follow them, download their pictures and be aware with everything that happens.

Join our secret society!

Enter /help to get all commands.
"""

UNREGISTERED = """
You was unregistered!
"""

NEW_GROUP_ADDED = """
*{0}* group created!
"""

GROUP_REMOVED = """
*{0}* group was removed!
"""

REGISTERED_GROUPS = """
Your groups:
"""

MEMBERS_GROUPS = """
Members from *{0}* group:
"""

NEW_USER_ADDED_TO_GROUP = """
The user(s) @{0} was added to *{1}* group!
"""

USER_REMOVED_FROM_GROUP = """
The user @{0} was removed from *{1}* group!
"""

HELP = """
/start   Welcome message
/help    Get all commands
/links   Some links
/about   Know about us

- Spy commands:
/register   Register as a spy
/unregister Unregister as a spy
/whoami     Informations about the spy

- Group commands:
/addgroup   Create a new group
/rmgroup    Remove an existing group
/groups     List all groups name
/updategroup Get the new photos from a group

- User commands:
/adduser    Add multiple users to a group
(USE COMMA TO ADD MORE THAN ONE USERS)
/rmuser     Remove a user from a group

- Shortcuts
Already know the group name and wanna get the new photos?
Use: $GROUP_NAME

Wanna get images from a user?
Use: @USERNAME
"""

LINKS = """\
Telegram:
https://telegram.me/@SpyList_bot

GitHub:
https://github.com/delete/spymanager
"""

START = """
Hey {0}, I'm the SpyManager bot.

I will help you to manage your users' groups.

Enter /help to get all commands.
"""

TELEGRAM_NOME_USUARIO_AJUDA = """

Você ainda não definiu o seu nome de usuário no Telegram.
Para defini-lo, vá na opção "Configurações" que fica no menu inicial do Telegram e modifique "Nome de usuário".

"""
TELEGRAM_ULTIMO_NOME_AJUDA = """

Você ainda não definiu o seu sobrenome no Telegram.
Para defini-lo, vá na opção "Configurações" que fica no menu inicial do Telegram, e modifique "sobrenome".

"""

BOT_PRIVADO = "Talk to me on private mode. "\
              "Send a message to @SpyList_bot and let's talk!"
