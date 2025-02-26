from __future__ import annotations

__all__ = ("TtsException", "NoTtsParameterException")


class TtsException(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)


class NoTtsParameterException(TtsException):
    def __init__(self, args: list[str] = []):
        super().__init__(
            "再生するファイルのパスを指定しない場合{}引数が必要です".format(
                ",".join(args)
            )
        )
