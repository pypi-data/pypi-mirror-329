from .common.singleton import Singleton


class Buffer(metaclass=Singleton):
    def __init__(self):
        self.__buffer: dict[str, any] = {}

    def set(self, key: str, value: any):
        self.__buffer[key] = value

    def get(self, key: str):
        return self.__buffer.get(key)

    def clear(self):
        self.__buffer = {}
