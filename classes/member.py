from typing import Tuple

import dateutil.parser

import util
import data_models.user
from data_models import guildmember


class GuildMember:
    def __init__(self, data: guildmember.GuildMember):
        if 'user' in data:
            self.user = User(data.get('user'))
        self.nick = data.get('nick')
        self.roles = data.get('roles')
        self.joined_at = util.parse_time(data.get('joined_at'))
        self.premium_since = util.parse_time(data.get('premium_since'))
        self.deaf = data.get('deaf')
        self.mute = data.get('mute')
        self.pending = data.get('pending')
        self.permissions = data.get('permissions')


class User:
    __slots__: Tuple[str, ...] = (
        'id', 'username', 'discriminator', 'avatar', 'bot', 'system', 'mfa_enabled', 'locale', 'verified', 'email',
        'flags',
        'premium_type', 'public_flags')

    def __init__(self, data: data_models.user.User):
        self.id = data.get('id')
        self.username = data.get('username')
        self.discriminator = data.get('discriminator')
        self.avatar = data.get('avatar')
        self.bot = data.get('bot')
        self.system = data.get('system')
        self.mfa_enabled = data.get('mfa_enabled')
        self.locale = data.get('locale')
        self.verified = data.get('verified')
        self.email = data.get('email')
        self.flags = data.get('flags')
        self.premium_type = data.get('premium_type')
        self.public_flags = data.get('public_flags')
