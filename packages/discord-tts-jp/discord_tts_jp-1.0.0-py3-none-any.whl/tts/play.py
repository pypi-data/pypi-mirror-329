from __future__ import annotations

import os

from discord import FFmpegPCMAudio, Message, VoiceClient

from .errors import NotFoundPlayFileException, NoTtsParameterException

__all__ = ("play",)


async def play(
    voice_client: VoiceClient,
    fp_voice_file: str | None = None,
    message: Message | None = None,
    ffmpeg_options: dict = {},
):
    """Voiceファイルを再生する

    再生後ファイルを削除する

    Parameters
    ----------
    voice_client : VoiceClient
        discord Voice Client
    fp_voice_file : str | None, optional
        ファイルパス。指定がない場合はmessageパラメータが必要
    message : Message | None, optional
        読み上げるメッセージのメッセージオブジェクト

    Raises
    ------
    NoTtsParameterException
        パラメータが足りないときのエラー
    NotFoundPlayFileException
        ファイルパスが適切に設定されてない時のエラー
    """

    if not fp_voice_file and not message:
        raise NoTtsParameterException(["message"])

    if not fp_voice_file and message:
        fp_voice_file = f"voices/{message.channel.id}/{message.id}.wav"

    if not fp_voice_file or not os.path.exists(fp_voice_file):
        raise NotFoundPlayFileException(fp_voice_file)

    voice_client.play(
        FFmpegPCMAudio(fp_voice_file, **ffmpeg_options),
        after=lambda _: os.remove(fp_voice_file),
    )
