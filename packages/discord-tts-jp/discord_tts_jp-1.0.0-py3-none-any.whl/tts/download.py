from __future__ import annotations

import json

import aiohttp

from .config import EMOTIONS, SPEAKERS
from .errors import MakeException
from .utils import logger


async def get_voice_byte(
    base_url: str,
    api_key: str,
    *,
    text: str,
    speaker: SPEAKERS,
    emotion: EMOTIONS | None = None,
    emotion_level: int | None = None,
    pitch: int,
    speed: int,
    volume: int = 100,
    author_id: int | None = None,
) -> bytes | None:
    """[VoiceText Web API](https://cloud.voicetext.jp/webapi/docs/api)合成音声を作成する

    Parameters
    ----------
    base_url : str
        VoiceText Web APIのベースURL

    api_key : str
        VoiceText Web APIのAPI key
    text : str
        読み上げるメッセージ内容
    speaker : str
        話者
    emotion : str
        感情(show以外必須)
    emotion_level : int
        感情(show以外必須)
    pitch : int
        音程
    speed : int
        速度 400だと結構早い
    volume : int
        音量
    author_id : int | None, optional
        ログに送信するためのメッセージ送信者ID

    Returns
    -------
    bytes | None
        合成音声データ

    Raises
    ------
    MakeException
        合成音声の作成に失敗した時のエラー
    """

    # 感情以外のエラーはレスポンスに任せる

    read_prm = {
        "text": text,
        "speaker": speaker,
        "pitch": pitch,
        "speed": speed,
        "volume": volume,
    }

    if speaker != "show":
        read_prm["emotion"] = emotion
        read_prm["emotion_level"] = emotion_level

    prm = {"url": base_url, "auth": aiohttp.BasicAuth(api_key), "params": read_prm}

    async with aiohttp.ClientSession() as session:
        async with session.post(**prm) as response:
            if response.status != 200:
                response_data = json.dumps(await response.json())
                if not response_data:
                    response_data = await response.text()

                logger.error(f"status={response.status} error={response_data}")
                raise MakeException(response.status, response_data)

            message = f"バイトサイズ: {response.content_length}"

            # 必要があればログにメッセージ送信者IDを含める
            if author_id:
                message += f"{author_id=}: {message}"

            logger.info(message)

            return await response.read()
