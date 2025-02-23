import secrets
import string

from line_works.mqtt.config import (
    CLIENT_ID_PREFIX,
    CLIENT_ID_SUFFIX_LENGTH,
    CONNECT_FLAGS,
    CONNECT_PACKET_TYPE,
    KEEP_ALIVE,
    PROTOCOL_LEVEL,
    PROTOCOL_NAME,
)


def generate_client_id_suffix() -> str:
    """ランダムなクライアントIDサフィックスを生成"""
    return "".join(
        secrets.choice(string.ascii_lowercase + string.digits)
        for _ in range(CLIENT_ID_SUFFIX_LENGTH)
    )


def generate_client_id() -> str:
    """クライアントIDを生成"""
    return CLIENT_ID_PREFIX + generate_client_id_suffix()


def create_connection_packet() -> bytes:
    """MQTT接続パケットを作成"""
    client_id = generate_client_id()
    payload_length = len(PROTOCOL_NAME) + 2 + len(client_id) + 2
    client_id_bytes = client_id.encode("ascii")

    return bytes(
        [
            CONNECT_PACKET_TYPE,  # パケットタイプ
            payload_length,  # 残りのパケット長
            0x00,
            0x04,  # プロトコル名長 (4バイト)
            *map(ord, PROTOCOL_NAME),  # "MQTT"のASCIIコード
            PROTOCOL_LEVEL,  # プロトコルレベル
            CONNECT_FLAGS,  # 接続フラグ
            0x00,  # キープアライブ MSB
            KEEP_ALIVE,  # キープアライブ LSB
            0x00,
            0x00,  # クライアントID長 (MSB, LSB)
            len(client_id),  # クライアントIDの長さ
            *client_id_bytes,  # クライアントID
        ]
    )
