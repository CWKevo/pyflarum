from typing import Optional

from datetime import datetime, timedelta

from .. import ExtensionMixin

from ...flarum.core.users import User, UserFromBulk
from ...error_handler import parse_request
from ...datetime_conversions import datetime_to_flarum, flarum_to_datetime


AUTHOR = 'flarum'
NAME = 'suspend'
ID = f"{AUTHOR}-{NAME}"

SOFT_DEPENDENCIES = []
HARD_DEPENCENDIES = []


class SuspendUserMixin(UserFromBulk):
    @property
    def canSuspend(self) -> bool:
        return self.attributes.get("canSuspend", False)


    @property
    def suspendedUntil(self):
        raw = self.attributes.get("suspendedUntil", None)

        return flarum_to_datetime(raw)


    def suspend(self, suspended_until: Optional[datetime]=None, suspended_for: Optional[timedelta]=None):
        if suspended_until:
            until = datetime_to_flarum(suspended_until)

        else:
            if suspended_for:
                now = datetime.now()
                raw_until = now + suspended_for

                until = datetime_to_flarum(raw_until)

            else:
                until = datetime_to_flarum(datetime(2069, 2, 6))


        post_data = {
            "data": {
                "type": "users",
                "id": "3",
                "attributes": {
                    "suspendedUntil": until
                }
            }
        }

        raw = self.user.session.patch(f"{self.user.api_urls['users']}/{self.id}", json=post_data)
        json = parse_request(raw)

        return User(user=self.user, _fetched_data=json)




class SuspendExtension(ExtensionMixin):
    def get_dependencies(self):
        return {
            "soft": SOFT_DEPENDENCIES,
            "hard": HARD_DEPENCENDIES
        }


    def mixin(self):
        super().mixin(self, UserFromBulk, SuspendUserMixin)
