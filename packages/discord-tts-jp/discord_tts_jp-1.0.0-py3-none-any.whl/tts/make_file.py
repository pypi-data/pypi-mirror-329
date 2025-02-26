from __future__ import annotations

import os

from .errors import NotFoundPlayFileException, NoTtsParameterException

__all__ = ("save_wave_file",)


async def save_wave_file(
    voice_byte: bytes,
    fp_voice_file: str | None = None,
    *,
    channel_id: int | None = None,
    message_id: int | None = None,
):
    """再生するファイルを作成する

    Parameters
    ----------
    voice_byte : bytes
        ファイルのバイト
    fp_voice_file : str | None, optional
        作成するファイルのパス
    channel_id : int | None, optional
        ファイルパスを自動生成する場合、チャンネルIDフォルダーを作成するためのチャンネルID
    message_id : int | None, optional
        ファイルパスを自動生成する場合、ファイル名のメッセージID

    Raises
    ------
    NoTtsParameterException
        パラメータが足りない時のエラー
    NotFoundPlayFileException
        ファイルパスが適切に設定されてない時のエラー
    """

    if not fp_voice_file and not channel_id and message_id:
        raise NoTtsParameterException(["voice_byte", "channel_id", "message_id"])

    if not fp_voice_file and (not channel_id or not message_id):
        raise NoTtsParameterException(["voice_byte", "channel_id", "message_id"])

    if not fp_voice_file and channel_id and message_id:
        fp_voice_file = f"voices/{channel_id}/{message_id}.wav"

    if not fp_voice_file or os.path.exists(fp_voice_file):
        raise NotFoundPlayFileException(fp_voice_file)

    if not os.path.isdir("voices"):
        os.mkdir("voices")

    if not os.path.isdir(f"voices/{channel_id}"):
        os.mkdir(f"voices/{channel_id}")

    with open(fp_voice_file, "wb") as f:
        f.write(voice_byte)
