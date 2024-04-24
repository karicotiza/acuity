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


class StringHexdigest:

    def __init__(self, string: str) -> None:
        self.__string: str = string
        self.__hexdigest: str = ''

    @property
    def value(self) -> str:
        if not self.__hexdigest:
            encoded: bytes = self.__string.encode()
            sha = sha256(encoded)
            self.__hexdigest = sha.hexdigest()

        return self.__hexdigest


class BytesHexdigest:

    def __init__(self, bytes_: bytes) -> None:
        self.__bytes: bytes = bytes_
        self.__hexdigest: str = ''

    @property
    def value(self) -> str:
        if not self.__hexdigest:
            sha = sha256(self.__bytes)
            self.__hexdigest = sha.hexdigest()

        return self.__hexdigest


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

    def __init__(self, data: bytes, hexdigest: str) -> None:
        self.__data = BytesIO(data)
        self.__hexdigest: str = hexdigest
        self.__text: str = ''

    @property
    def text(self) -> str:
        if not self.__text:
            started: str = services.cache.get_started(self.__hexdigest)

            if started:
                return ''

            cached_result: str = services.cache.get_finished(self.__hexdigest)

            if cached_result:
                self.__text = cached_result

            else:
                services.cache.set_started(self.__hexdigest, 'True')

                self.__data = services.converter.convert(self.__data)
                result: str = services.recognition.recognize(self.__data)
                self.__text = result

                services.cache.set_finished(self.__hexdigest, self.__text)

        return self.__text


class Base64:

    def __init__(self, value: str) -> None:
        self.__value = value

    def to_bytes(self) -> bytes:
        result: bytes = services.decoder.decode_base64(self.__value)
        return result
