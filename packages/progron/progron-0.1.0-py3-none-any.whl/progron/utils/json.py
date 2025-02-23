from typing import Any, Callable, Final

from msgspec.json import Decoder, Encoder

mjson_decode: Final[Callable[..., Any]] = Decoder[dict[str, Any]]().decode
encode_bytes: Final[Callable[..., bytes]] = Encoder().encode


def mjson_encode(obj: Any) -> str:
    data: bytes = encode_bytes(obj)
    return data.decode()
