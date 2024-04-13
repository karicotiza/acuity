import typing

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import viewsets, status, mixins
from rest_framework.serializers import BaseSerializer
from rest_framework.response import Response
from logic.api.serializers.file import FileSerializer
from logic.models import AudioData, BytesIO


class FileViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class: typing.Type[FileSerializer] = FileSerializer

    def create(self, request, *args, **kwargs) -> Response:
        post: BaseSerializer = self.get_serializer(data=request.data)
        post.is_valid(raise_exception=True)
        headers: dict = self.get_success_headers(post.validated_data)

        file: InMemoryUploadedFile = post.validated_data.get('file')

        bytes_io: BytesIO | typing.Any = file.file

        if isinstance(bytes_io, BytesIO):
            bytes_: bytes = bytes_io.read()

        audio_data: AudioData = AudioData(bytes_)

        data: dict = {'status': audio_data.recognize()}

        response: Response = Response(
            data=data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

        return response
