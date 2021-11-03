from typing import List, Optional

import data_models.guild
from classes.channel import Channel
from classes.member import GuildMember
from classes.role import Role
from util import api_call, DiscordAPIError


class GuildPreview:
    def __init__(self, data: data_models.guild.GuildPreview):
        self.id: str = data.get('id')
        self.name: str = data.get('name')
        self.icon: Optional[str] = data.get('icon')
        self.splash: Optional[str] = data.get('splash')
        self.discovery_splash: Optional[str] = data.get('discovery_splash')
        self.emojis: List[dict] = data.get('emojis')
        self.features: List[str] = data.get('features')
        self.approximate_member_count: int = data.get('approximate_member_count')
        self.approximate_presence_count: int = data.get('approximate_presence_count')
        self.description: Optional[str] = data.get('description')


class Guild:
    def __init__(self, data: data_models.guild.Guild):
        self.id: str = data.get('id')
        self.name: str = data.get('name')
        self.icon = data.get('icon')
        self.icon_hash = data.get('icon_hash')
        self.splash = data.get('splash')
        self.discovery_splash = data.get('discovery_splash')
        self.owner = data.get('owner')
        self.owner_id = data.get('owner_id')
        self.permissions = data.get('permissions')
        self.region = data.get('region')
        self.afk_channel_id = data.get('afk_channel_id')
        self.afk_timeout = data.get('afk_timeout')
        self.widget_enabled = data.get('widget_enabled')
        self.widget_channel_id = data.get('widget_channel_id')
        self.verification_level = data.get('verification_level')
        self.default_message_notifications = data.get('default_message_notifications')
        self.explicit_content_filter = data.get('explicit_content_filter')
        if 'roles' in data:
            roles_list = []
            for i in data.get('roles'):
                role = Role(i)
                roles_list.append(role)
            self.roles: List[Role] = roles_list
        self.emojis = data.get('emojis')
        self.features = data.get('features')
        self.mfa_level = data.get('mfa_level')
        self.application_id = data.get('application_id')
        self.system_channel_id = data.get('system_channel_id')
        self.system_channel_flags = data.get('system_channel_flags')
        self.rules_channel_id = data.get('rules_channel_id')
        self.joined_at = data.get('joined_at')
        self.large = data.get('large')
        self.unavailable = data.get('unavailable')
        self.member_count = data.get('member_count')
        self.voice_states = data.get('voice_states')
        self.members = data.get('members')
        self.channels = data.get('channels')
        self.threads = data.get('threads')
        self.presences = data.get('presences')
        self.max_presences = data.get('max_presences')
        self.max_members = data.get('max_members')
        self.vanity_url_code = data.get('vanity_url_code')
        self.description = data.get('description')
        self.banner = data.get('banner')
        self.premium_tier = data.get('premium_tier')
        self.premium_subscription_count = data.get('premium_subscription_count')
        self.preferred_locale = data.get('preferred_locale')
        self.public_updates_channel_id = data.get('public_updates_channel_id')
        self.max_video_channel_users = data.get('max_video_channel_users')
        self.approximate_member_count = data.get('approximate_member_count')
        self.approximate_presence_count = data.get('approximate_presence_count')
        self.welcome_screen = data.get('welcome_screen')
        self.nsfw_level = data.get('nsfw_level')
        self.stage_instances = data.get('stage_instances')
        self.stickers = data.get('stickers')

    async def add_role(self, name: str = None, permissions: str = None, color: int = None, hoist: bool = None,
                       mentionable: bool = None):
        json_role = await api_call(f'/guilds/{self.id}/roles', 'POST',
                                   json={'name': name, 'permissions': permissions, 'color': color, 'hoist': hoist,
                                         'mentionable': mentionable})
        role = Role(json_role)
        self.roles.append(role)
        return role

    async def list_members(self, limit=1, after='0') -> List[GuildMember]:
        """Returns a list of :py:class:`classes.member.GuildMember` objects"""
        members = await api_call(f'/guilds/{self.id}/members?limit={limit}&after={after}', 'GET')
        member_list = []
        if isinstance(members, list):
            for i in members:
                member_list.append(GuildMember(i))
        return member_list

    async def get_preview(self):
        try:
            response = await api_call(f'/guild/{self.id}', 'GET')
        except DiscordAPIError as e:
            return None
        return GuildPreview(response)

    async def modify(self,
                     name: str = None,
                     region: Optional[str] = None,
                     verification_level: data_models.guild.VerificationLevel = None,
                     default_message_notifications: data_models.guild.DefaultMessageNotificationLevel = None,
                     explicit_content_filter: data_models.guild.ExplicitContentFilterLevel = None,
                     afk_channel_id: Optional[str] = None,
                     afk_timeout: int = None,
                     icon: Optional[str] = None,
                     owner_id: str = None,
                     splash: Optional[str] = None,
                     discovery_splash: Optional[str] = None,
                     banner: Optional[str] = None,
                     system_channel_id: Optional[str] = None,
                     system_channel_flags: int = None,
                     rules_channel_id: Optional[str] = None,
                     public_updates_channel_id: Optional[str] = None,
                     preferred_locale: Optional[str] = None,
                     features: List[str] = None,
                     description: Optional[str] = None,
                     ):
        options = {}
        if name is not None:
            options['name'] = name
        if region is not None:
            options['region'] = region
        if verification_level is not None:
            options['verification_level'] = verification_level
        if default_message_notifications is not None:
            options['default_message_notifications'] = default_message_notifications
        if explicit_content_filter is not None:
            options['explicit_content_filter'] = explicit_content_filter
        if afk_channel_id is not None:
            options['afk_channel_id'] = afk_channel_id
        if afk_timeout is not None:
            options['afk_timeout'] = afk_timeout
        if icon is not None:
            options['icon'] = icon
        if owner_id is not None:
            options['owner_id'] = owner_id
        if splash is not None:
            options['splash'] = splash
        if discovery_splash is not None:
            options['discovery_splash'] = discovery_splash
        if banner is not None:
            options['banner'] = banner
        if system_channel_id is not None:
            options['system_channel_id'] = system_channel_id
        if system_channel_flags is not None:
            options['system_channel_flags'] = system_channel_flags
        if rules_channel_id is not None:
            options['rules_channel_id'] = rules_channel_id
        if public_updates_channel_id is not None:
            options['public_channel_id'] = public_updates_channel_id
        if preferred_locale is not None:
            options['preferred_locale'] = preferred_locale
        if features is not None:
            options['features'] = features
        if description is not None:
            options['description'] = description

        try:
            response = await api_call(f'/guild/{self.id}', 'PATCH', json=options)
        except DiscordAPIError as e:
            return None
        return Guild(response)

    async def delete(self):
        try:
            response = await api_call(f'/guild/{self.id}', 'DELETE')
        except DiscordAPIError as e:
            return None
        return response

    async def get_channels(self):
        try:
            response = await api_call(f'/guild/{self.id}/channels', 'GET')
        except DiscordAPIError as e:
            return None
        channels = []
        for i in response:
            channels.append(Channel(i))
        return channels


async def get_guild(guild_id: id) -> Optional[Guild]:
    try:
        response = await api_call(f'/guild/{guild_id}', 'GET')
    except DiscordAPIError as e:
        return None
    return Guild(response)
