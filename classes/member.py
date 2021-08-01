import datetime
import dateutil.parser


class GuildMember:
    def __init__(self):
        self.user = None
        self.nick = None
        self.roles = None
        self.joined_at = None
        self.premium_since = None
        self.deaf = None
        self.mute = None
        self.pending = None
        self.permissions = None


async def load_guild_member(data: dict):
    member = GuildMember()
    if data.get('user') is None:
        member.user = None
    else:
        member.user = await load_user(data.get('user'))
    member.nick = data.get('nick')
    member.roles = data.get('roles')
    member.joined_at = dateutil.parser.parse(str(data.get('joined_at')))
    if data.get('premium_since') is None:
        member.premium_since = None
    else:
        member.premium_since = dateutil.parser.parse(
            data.get('premium_since'))
    member.deaf = data.get('deaf')
    member.mute = data.get('mute')
    member.pending = data.get('pending')
    member.permissions = data.get('permissions')

    return member


class User:
    def __init__(self):
        self.id = None
        self.username = None
        self.discriminator = None
        self.avatar = None
        self.bot = None
        self.system = None
        self.mfa_enabled = None
        self.locale = None
        self.verified = None
        self.email = None
        self.flags = None
        self.premium_type = None
        self.public_flags = None


async def load_user(data: dict):
    user = User()
    user.id = data.get('id')
    user.username = data.get('username')
    user.discriminator = data.get('discriminator')
    user.avatar = data.get('avatar')
    user.bot = data.get('bot')
    user.system = data.get('system')
    user.mfa_enabled = data.get('mfa_enabled')
    user.locale = data.get('locale')
    user.verified = data.get('verified')
    user.email = data.get('email')
    user.flags = data.get('flags')
    user.premium_type = data.get('premium_type')
    user.public_flags = data.get('public_flags')

    return user
