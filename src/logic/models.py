from io import BytesIO
from hashlib import sha256
from django.db import models
from django.core.handlers.wsgi import WSGIRequest
from django.core.validators import MinLengthValidator
from logic import services

# Create your models here.


class IP:

    def __init__(self, request: WSGIRequest) -> None:
        self.__request: WSGIRequest = request
        self.__ip: str = ''

    @property
    def value(self) -> str:

        if not self.__ip:
            forwarded_for: str = self.__request.META.get(
                'HTTP_X_FORWARDED_FOR', ''
            )

            if forwarded_for:
                self.__ip = forwarded_for.split(',')[0]

            else:
                self.__ip = self.__request.META.get('REMOTE_ADDR', '')

        return self.__ip


class Hash:

    def __init__(self, string: str) -> None:
        self.__string: str = string

    @property
    def value(self) -> str:
        encoded: bytes = self.__string.encode()
        sha = sha256(encoded)
        hexdigest: str = sha.hexdigest()

        return hexdigest


class Logs(models.Model):
    ip: models.GenericIPAddressField = models.GenericIPAddressField(
        protocol='IPv4',
        blank=False,
    )

    timestamp: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        blank=False
    )

    hash: models.CharField = models.CharField(
        blank=False,
        max_length=64,
        validators=[
            MinLengthValidator(64),
        ],
    )


class AudioData:

    def __init__(self, data: bytes) -> None:
        self.__data = BytesIO(data)
        self.__convert()

    def __convert(self) -> None:
        self.__data = services.converter.convert(self.__data)

    def recognize(self) -> str:
        result: str = services.recognition.recognize(self.__data)
        return result


class Base64:

    def __init__(self, value: str) -> None:
        self.__value = value

    def to_bytes(self) -> bytes:
        result: bytes = services.decoder.decode_base64(self.__value)
        return result
