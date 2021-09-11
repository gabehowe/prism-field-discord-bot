from typing import List

import data_models.guild
from classes.role import Role
from util import api_call


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
        await api_call(f'/guilds/{self.id}/roles', 'POST',
                       json={'name': name, 'permissions': permissions, 'color': color, 'hoist': hoist,
                             'mentionable': mentionable})
