from typing import Union

from normalize_path import normalize_path
normalize_path()

from dotenv import load_dotenv
load_dotenv()

import os
import time

from pyflarum import FlarumUser

from pyflarum.extensions import absolutely_all
from pyflarum.extensions.flarum import Flarum_Approval


EXTENSIONS = [
    absolutely_all.AbsolutelyAllExtension,
    Flarum_Approval.ApprovalExtension
]


user = FlarumUser(forum_url=os.environ['forum_url'], username='test', password=os.environ['account_password'], extensions=EXTENSIONS) # type: absolutely_all.AbsolutelyAllFlarumUserMixin


if __name__ == "__main__":
    for discussions in user.absolutely_all_discussions():
        discussion: Union[Flarum_Approval.ApprovalDiscussionFromNotificationMixin]

        for discussion in discussions:
            time.sleep(5) # prevent 429
            full_discussion = discussion.get_full_data()

            for post in full_discussion.get_posts():
                post: Flarum_Approval.ApprovalPostFromNotificationMixin

                if not post.isApproved:
                    post.approve()
                    print(f"Approved {post.url}")
