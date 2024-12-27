"""
Configuration for Ivy
"""
from __future__ import annotations
from typing import List


class Account:
    token: str = ""
    developers: List[int] = [
        1017020135585873961,
        1017021900137971752,
        957473718018392207
    ]
    version: int = 1
    prefix: str = ","

class Emoji:
    approve: str = "<:approve:1320599091385864323>"
    deny: str = "<:deny:1320599114399879238>"
    warn: str = "<:warn:1320599131902709880>"

class Color:
    green: int = 0xa4eb78
    red: int = 0xf94848
    yellow: int = 0xffC64A
    info: int = 0x767F8C