import typing

from django.urls import reverse
from rest_framework import viewsets, status, mixins
from rest_framework.serializers import BaseSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from logic.api.serializers.base64 import Base64Serializer
from logic.api.serializers.link import LinkSerializer
from logic.models import Base64, IP, BytesHexdigest
from logic.tasks import start_recognition


class Base64ViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class: typing.Type[Base64Serializer] = Base64Serializer

    @extend_schema(
        request=Base64Serializer,
        responses={201: LinkSerializer},
    )
    def create(self, request, *args, **kwargs) -> Response:
        post: BaseSerializer = self.get_serializer(data=request.data)
        post.is_valid(raise_exception=True)
        headers: dict = self.get_success_headers(post.validated_data)

        base64: str = post.validated_data.get('base64')
        base64_: Base64 = Base64(base64)
        bytes_: bytes = base64_.to_bytes()

        audio_bytes_hexdigest: BytesHexdigest = BytesHexdigest(bytes_)
        ip: IP = IP(request)

        start_recognition.delay(bytes_, audio_bytes_hexdigest.value, ip.value)

        link: str = self.__generate_text_link(
            request, audio_bytes_hexdigest.value
        )

        response_data: LinkSerializer = LinkSerializer(
            data={'link': link}
        )

        response_data.is_valid()

        response: Response = Response(
            data=response_data.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

        return response

    def __generate_text_link(self, request, hexdigest: str) -> str:
        relative_link: str = reverse('logic:text-detail', args=[hexdigest])
        absolute_link: str = request.build_absolute_uri(relative_link)

        return absolute_link
