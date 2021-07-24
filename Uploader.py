from abc import ABC, abstractmethod


class Uploader(ABC):
    @abstractmethod
    def upload(self, data: dict):
        pass
