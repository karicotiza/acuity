import typing

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import viewsets, status, mixins
from rest_framework.serializers import BaseSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from logic.api.serializers.file import FileSerializer
from logic.api.serializers.text import TextSerializer
from logic.models import AudioData, BytesIO, Logs, IP, Hash


class FileViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class: typing.Type[FileSerializer] = FileSerializer

    @extend_schema(
        request=FileSerializer,
        responses={201: TextSerializer},
    )
    def create(self, request, *args, **kwargs) -> Response:
        post: BaseSerializer = self.get_serializer(data=request.data)
        post.is_valid(raise_exception=True)
        headers: dict = self.get_success_headers(post.validated_data)

        file: InMemoryUploadedFile = post.validated_data.get('file')

        bytes_io: BytesIO | typing.Any = file.file

        if isinstance(bytes_io, BytesIO):
            bytes_: bytes = bytes_io.read()

        audio_data: AudioData = AudioData(bytes_)

        text = audio_data.recognize()
        ip: IP = IP(request)
        sha: Hash = Hash(text)
        logs: Logs = Logs(ip=ip.value, hash=sha.value)
        logs.save()

        response_data: TextSerializer = TextSerializer(
            data={'text': text}
        )

        response_data.is_valid()

        response: Response = Response(
            data=response_data.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

        return response
