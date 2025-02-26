from __future__ import annotations

from .shared import TtsException

__all__ = ("AuthFailedException",)


class AuthFailedException(TtsException):
    def __init__(self):
        super().__init__("認証情報が不正です。")
