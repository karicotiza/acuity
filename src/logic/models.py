from io import BytesIO
from django.db import models
from logic import services

# Create your models here.


class AudioData:

    def __init__(self, data: bytes) -> None:
        self.__data = BytesIO(data)

    def recognize(self) -> str:
        result: str = services.recognition.recognize(self.__data)
        return result


class Base64:

    def __init__(self, value: str) -> None:
        self.__value = value

    def to_bytes(self) -> bytes:
        result: bytes = services.decoder.decode_base64(self.__value)
        return result
