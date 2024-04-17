from django.core.cache import cache


class Cache:

    def __init__(self) -> None:
        pass

    def get(self, key: str) -> str:
        value = cache.get(key, '')

        if value:
            cache.touch(key)

        return value

    def set(self, key: str, value: str) -> None:
        cache.set(key, value)
