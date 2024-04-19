from django.core.cache import cache


class Cache:

    def __init__(self) -> None:
        pass

    def get_started(self, key: str) -> str:
        result = self.__get(key, 1)
        return result

    def get_finished(self, key: str) -> str:
        result = self.__get(key, 2)
        return result

    def __get(self, key: str, version: int) -> str:
        value = cache.get(key, '', version=version)

        if value:
            cache.touch(key, version=version)

        return value

    def set_started(self, key: str, value: str) -> None:
        self.__set(key, value, 1)

    def set_finished(self, key: str, value: str) -> None:
        self.__set(key, value, 2)

    def __set(self, key: str, value: str, version: int) -> None:
        cache.set(key, value, version=version)
