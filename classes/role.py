from typing import Optional

from data_models import roles


class Role:
    def __init__(self, data: (roles.Role, str)):
        if isinstance(data, str):
            self.id = data
            return
        self.id = data.get('id')
        self.name: str = data.get('name')
        self.color = data.get('color')
        self.hoist: bool = data.get('hoist')
        self.position: int = data.get('position')
        self.permissions: str = data.get('permissions')
        self.managed: bool = data.get('managed')
        self.mentionable: bool = data.get('mentionable')
        if 'tags' in data:
            self.tags = RoleTags(data.get('tags'))


class RoleTags:
    def __init__(self, data: roles.RoleTags):
        self.bot_id: Optional[str] = data.get('bot_id')
        self.integration_id: Optional[str] = data.get('integration_id')
        self.premium_subscriber: Optional = data.get('premium_subscriber')
