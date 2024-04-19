from io import BytesIO
from base64 import b64decode, b64encode
from rest_framework import serializers
from logic.models import Base64
from pydub import AudioSegment  # type: ignore


class Base64Serializer(serializers.Serializer):
    base64: serializers.CharField = serializers.CharField()

    def validate_base64(self, data: str) -> str:
        try:
            decoded_bytes: bytes = b64decode(data)
            encoded_bytes: bytes = b64encode(decoded_bytes)
            converted: str = str(encoded_bytes)
            converted = converted[2:-1]

            if data != converted:
                raise serializers.ValidationError('Malformed base64 data.')

        except Exception:
            raise serializers.ValidationError('Malformed base64 data.')

        try:
            base64_: Base64 = Base64(data)
            bytes_io: BytesIO = BytesIO(base64_.to_bytes())

            AudioSegment.from_file(bytes_io)
        except Exception:
            raise serializers.ValidationError('Not an audio.')

        return data
