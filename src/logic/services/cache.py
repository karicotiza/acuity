from django.core.cache import cache


class Cache:

    def __init__(self) -> None:
        pass

    def get_started(self, key: str) -> str:
        result = cache.get(key, '', version=1)
        return result

    def get_finished(self, key: str) -> str:
        result = cache.get(key, '', version=2)
        return result

    def set_started(self, key: str, value: str) -> None:
        cache.set(key, value, None, 1)

    def set_finished(self, key: str, value: str) -> None:
        cache.set(key, value, version=2)
        cache.set(key, value, version=1)

    def refresh(self, key: str) -> None:
        cache.touch(key, version=1)
        cache.touch(key, version=2)
