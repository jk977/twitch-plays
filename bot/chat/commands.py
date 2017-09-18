import config
import re
import sys
import utils

from settings import Settings

from chat.permissions import permissions
from chat.roles import Roles
from chat.user import User


class Command:
    def __init__(self, action=None, **kwargs):
        if not callable(action):
            raise TypeError('"action" must be callable.')

        self._action = action
        self._kwargs = kwargs

    def run(self):
        self._action(**self._kwargs)


def get_roles(chat, user, args):
    roles = []

    if user.is_moderator:
        roles.append('moderator')
    if user.is_owner:
        roles.append('owner')
    if user.is_banned:
        roles.append('banned')

    msg = 'Your roles are: '

    if roles:
        msg += ', '.join(roles)
    else:
        msg += 'default'

    chat.send_message(msg)


def get_song(chat, user, args):
    chat.send_message('Dragon Quest 1 and 2 Symphonic Suites - https://www.youtube.com/playlist?list=PL2jLKwo6ZTmQ0vKgGwbcp5m2sp7vy9GXY')


@permissions(Roles.DEFAULT)
def get_banlist(chat, user, args):
    banlist = [u.name for u in config.users.values() if u.is_banned]

    if len(banlist) == 0:
        message = 'No one is currently banned.'
    else:
        message = 'Banned users: ' + ', '.join(banlist)

    chat.send_message(message)


@permissions(Roles.DEFAULT)
def get_gil(chat, user, args):
    with open('../game/gil.txt', 'r') as file:
        gil = file.read()

    chat.send_message('{:,}'.format(int(gil)))


@permissions(Roles.DEFAULT)
def get_help(chat, user, args):
    with open('info/help.cfg', 'r') as file:
        help_msg = file.read().strip();
    chat.send_message(help_msg)


@permissions(Roles.DEFAULT)
def get_map(chat, user, args):
    chat.send_message('https://i.imgur.com/mkotcf9.png')


@permissions(Roles.DEFAULT)
def get_mods(chat, user, args):
    mod_list = [u.name for u in config.users.values() if u.is_moderator]

    if len(mod_list) == 0:
        message = 'No moderators currently.'
    else:
        message = 'Moderators: ' + ', '.join(mod_list)

    chat.send_message(message)


@permissions(Roles.DEFAULT)
def get_threshold(chat, user, args):
    threshold = config.vm.threshold
    chat.send_message('The vote threshold is currently {}.'.format(threshold))


@permissions(Roles.MOD, silent=True)
def ban(chat, user, args):
    def true_ban(name):
        """Contains ban logic."""
        name = name.lower().replace('@', '').strip()

        if not name in config.users:
            target = User(name=name)
            config.users[name] = target
        else:
            target = config.users[name]
            
        if user.role > target.role:
            target.ban()
            return True
        else:
            return False


    args = [utils.extract_username(user) for user in args]
    banned_users = []

    if user.is_owner:
        for name in args:
            if true_ban(name):
                banned_users.append(name)
    else:
        if true_ban(args[0]):
            banned_users = [args[0]]

    if banned_users:
        chat.send_message('Banned {}.'.format(', '.join(banned_users)))
    

@permissions(Roles.MOD, silent=True)
def unban(chat, user, args):
    args = [utils.extract_username(user) for user in args]
    unbanned_list = []

    for name in args:
        target = config.users.get(name, None)

        if target and target.is_banned:
            target.unban()
            unbanned_list.append(name)

    if unbanned_list:
        chat.send_message('Unbanned {}.'.format(', '.join(unbanned_list)))


@permissions(Roles.OWNER, silent=True)
def restart(chat, user, args):
    chat.send_message('Restarting chat bot... Inputs won\'t work until restart is finished.')
    Settings.save_settings()
    config.threads.stop_all_threads()
    chat.close()
    sys.exit(0)


@permissions(Roles.OWNER, silent=True)
def mod(chat, user, args):
    args = [utils.extract_username(user) for user in args]

    for name in args:
        if not name in config.users:
            target = User(name=name)
            config.users[name] = target
        else:
            target = config.users[name]
            
        target.mod()


@permissions(Roles.OWNER, silent=True)
def unmod(chat, user, args):
    args = [utils.extract_username(user) for user in args]

    for name in args:
        target = config.users.get(name, None)

        if target:
            target.unmod()


@permissions(Roles.OWNER, silent=True)
def prune(chat, user, args):
    for user in [u for u in config.users.values() if u.role == 2 and not u.choice]:
        del config.users[user.name]
    chat.send_message('Removed inactive users.')
