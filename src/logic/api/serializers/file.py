from io import BytesIO
from typing import Any
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from pydub import AudioSegment  # type: ignore


class FileSerializer(serializers.Serializer):
    file: serializers.FileField = serializers.FileField()

    def validate_file(
        self, file: InMemoryUploadedFile
    ) -> InMemoryUploadedFile:
        too_long: bool = False

        try:
            bytes_io: BytesIO | Any = file.file

            if isinstance(bytes_io, BytesIO):
                bytes_: bytes = bytes_io.read()
                bytes_io.seek(0)

            bytes_io_: BytesIO = BytesIO(bytes_)

            audio = AudioSegment.from_file(bytes_io_)

            if audio.duration_seconds > 30:
                too_long = True

        except Exception:
            raise serializers.ValidationError('Not an audio file.')

        if too_long:
            message: str = 'The audio should be shorter than 30 seconds.'
            raise serializers.ValidationError(message)

        return file
