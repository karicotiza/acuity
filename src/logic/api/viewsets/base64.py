import typing

from rest_framework import viewsets, status, mixins
from rest_framework.serializers import BaseSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from logic.api.serializers.base64 import Base64Serializer
from logic.api.serializers.text import TextSerializer
from logic.models import AudioData, Base64


class Base64ViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class: typing.Type[Base64Serializer] = Base64Serializer

    @extend_schema(
        request=Base64Serializer,
        responses={201: TextSerializer},
    )
    def create(self, request, *args, **kwargs) -> Response:
        post: BaseSerializer = self.get_serializer(data=request.data)
        post.is_valid(raise_exception=True)
        headers: dict = self.get_success_headers(post.validated_data)

        base64: str = post.validated_data.get('base64')
        base64_: Base64 = Base64(base64)
        audio_data: AudioData = AudioData(base64_.to_bytes())

        response_data: TextSerializer = TextSerializer(
            data={'text': audio_data.recognize()}
        )

        response_data.is_valid()

        response: Response = Response(
            data=response_data.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

        return response
