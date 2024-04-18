import typing

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from logic.api.serializers.text import TextSerializer
from logic import services


class TextViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class: typing.Type[TextSerializer] = TextSerializer

    @extend_schema(
        responses={201: TextSerializer},
    )
    def retrieve(self, request, *args, **kwargs) -> Response:
        id: str = kwargs['pk']
        audio_hexdigest = id

        ready: bool = False
        text: str = services.cache.get(audio_hexdigest)

        if text:
            ready = True

        response_data: TextSerializer = TextSerializer(
            data={'ready': ready, 'text': text}
        )

        response_data.is_valid()

        response: Response = Response(data=response_data.data)

        return response
