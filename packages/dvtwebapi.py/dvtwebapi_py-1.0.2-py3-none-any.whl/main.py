from __future__ import annotations

from discord import Message, VoiceClient

from . import config
from .download import get_voice_byte
from .errors import AuthFailedException
from .make_file import save_wave_file
from .play import play
from .utils import logger

__all__ = ("Tts",)


class Tts:
    def __init__(
        self,
        base_url: str | None = config.BASE_URL,
        api_key: str | None = config.API_KEY,
    ):
        self.api_key = api_key
        self.base_url = base_url

    async def download_voice_byte(
        self,
        text: str,
        *,
        speaker: config.SPEAKERS,
        emotion: config.EMOTIONS | None = None,
        emotion_level: int | None = None,
        pitch: int,
        speed: int,
        volume: int = 100,
        author_id: int | None = None,
    ):
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

        AuthFailedException
            認証情報が不正なときのエラー
        """

        if not isinstance(self.base_url, str):
            raise AuthFailedException()
        if not isinstance(self.api_key, str):
            raise AuthFailedException()

        logger.debug(f"合成音声作成開始: {author_id=} t={text[:30]}")

        return await get_voice_byte(
            self.base_url,
            self.api_key,
            text=text,
            speaker=speaker,
            emotion=emotion,
            emotion_level=emotion_level,
            pitch=pitch,
            speed=speed,
            volume=volume,
            author_id=author_id,
        )

    async def save_wave_file(
        self,
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

        message = f"bynary_length={len(voice_byte)} "

        if fp_voice_file:
            message += f"{fp_voice_file=}"
        else:
            message += f"{channel_id=} {message_id=}"

        logger.debug(f"ファイル作成開始: {message}")

        return await save_wave_file(
            voice_byte, fp_voice_file, channel_id=channel_id, message_id=message_id
        )

    async def play(
        self,
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

        log_message = f"再生: {fp_voice_file=} "

        if message:
            log_message += f"t={message.content[:30]}"

        logger.debug(log_message)

        return await play(voice_client, fp_voice_file, message, ffmpeg_options)
