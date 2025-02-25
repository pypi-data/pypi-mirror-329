from enum import Enum
from typing import Dict


class ImageFmt(Enum):
    Png: Dict[str, str] = {"pil": "PNG", "cv": ".png"}
    Jpg: Dict[str, str] = {"pil": "JPG", "cv": ".jpg"}


class Payload(Enum):
    Dict: str = "dict"
    OnData: str = "on_data"
    OnEmit: str = "on_emit"


class LogMessage(Enum):
    Instance: str = "初回のインスタンス生成には引数appが必要です。"
    Mounted: str = "既に「{}」はマウントされています。"
    NotExist: str = "「{}」はマウントされていません。"
    NoEvent: str = "登録されたメソッドはありません。"
    AttrErr: str = "メソッド「{}」は存在しません。"
    Register: str = "メソッド「{}」を登録しました。"
    Activate: str = "「{}」メソッドを{}イベントに登録しました。"
