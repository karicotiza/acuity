from base64 import b64decode


class Decoder:

    def __init__(self) -> None:
        pass

    def decode_base64(self, value: str) -> bytes:
        result: bytes = b64decode(value.encode())
        return result
