from typing import List, Optional

import data_models.presence


class Activity:
    def __init__(self, data: data_models.presence.Activity):
        self.url: Optional[str] = data.get('url')
        self.name: Optional[str] = data.get('name')
        self.type: Optional[data_models.presence.ActivityType] = data.get('type')


class Presence:
    def __init__(self, data: data_models.presence.GatewayPresenceUpdate):
        self.since: int = data.get('since')
        self.status: data_models.presence.Status = data.get('status')
        self.afk: bool = data.get('afk')
        if 'activities' in data:
            self.activities: List[Activity] = []
            for i in data.get('activities'):
                if isinstance(i, dict):
                    self.activities.append(Activity(i))
                elif isinstance(i, Activity):
                    self.activities.append(i)
