from rest_framework import serializers


class TextSerializer(serializers.Serializer):
    ready: serializers.BooleanField = serializers.BooleanField()
    text: serializers.CharField = serializers.CharField(allow_blank=True)
