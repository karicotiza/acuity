from rest_framework import serializers


class Base64Serializer(serializers.Serializer):
    base64: serializers.CharField = serializers.CharField()
