import typing

from django.http import Http404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from logic.api.serializers.text import TextSerializer
from logic import services


class TextViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class: typing.Type[TextSerializer] = TextSerializer

    @extend_schema(
        responses={200: TextSerializer},
        parameters=[
            OpenApiParameter(
                name="id", type=str, location=OpenApiParameter.PATH
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs) -> Response:
        id: str = kwargs['pk']
        audio_hexdigest = id

        started: str = services.cache.get_started(audio_hexdigest)

        if not started:
            raise Http404()

        else:
            ready: bool = False
            text: str = services.cache.get_finished(audio_hexdigest)

            if text:
                ready = True
                services.cache.refresh(audio_hexdigest)

            response_data: TextSerializer = TextSerializer(
                data={'ready': ready, 'text': text}
            )

            response_data.is_valid(raise_exception=True)

            response = Response(data=response_data.data)

            return response
