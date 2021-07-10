from typing import List

from . import ExtensionMixin
from ..session import FlarumUser

import re


class CommandsFlarumUserMixin(FlarumUser):
    def is_mentioned_in(self, string: str):
        match = re.search(rf'@"({self.username})"#[a-z0-9]+', string)

        if match:
            return True

        else:
            return False


    def parse_as_command(self, string: str, is_mentioned: bool=True, split_at: str=' '):
        """
            Parses a command from a string (e. g.: post's content). The result is list of arguments.

            ### Example:
            ```python
                user.parse_command()
            ```
        """

        if self.is_mentioned_in(string) and is_mentioned:
            match = re.search(rf'@"{self.username}"#[a-z0-9]+\s(.+)', string)

            if match:
                group = match.group(1)

                if group:
                    parsed = group.split(sep=split_at) # type: List[str]

                    return parsed

        return string.split(sep=split_at)


class CommandsExtension(ExtensionMixin, CommandsFlarumUserMixin):
    def mixin(self):
        super().mixin(self, FlarumUser, CommandsFlarumUserMixin)
