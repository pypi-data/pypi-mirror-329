from __future__ import annotations

from .shared import TtsException

__all__ = ("NotFoundPlayFileException", "MakeException")


class NotFoundPlayFileException(TtsException):
    def __init__(self, fp: str | None):
        super().__init__(f"再生するファイルが見つかりませんでした。{fp=}")


class MakeException(TtsException):
    def __init__(self, status: int, data: dict | str):
        super().__init__(f"合成音声データの取得に失敗しました。{status=} {data=}")
