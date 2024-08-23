import abc

from requests import Response, Session


class AbstractRequester(Session, metaclass=abc.ABCMeta):
    def __init__(self, first_part_url: str = ''):
        super().__init__()
        self.first_part_url = first_part_url

    @abc.abstractmethod
    def get(self, url: str = '', **kwargs) -> Response:
        return super().get(url=self.first_part_url + url, **kwargs)

    @abc.abstractmethod
    def post(self, url: str = '', **kwargs) -> Response:
        return super().post(url=self.first_part_url + url, **kwargs)

    @abc.abstractmethod
    def put(self, url: str = '', **kwargs) -> Response:
        return super().put(url=self.first_part_url + url, **kwargs)

    @abc.abstractmethod
    def patch(self, url: str = '', **kwargs) -> Response:
        return super().patch(url=self.first_part_url + url, **kwargs)

    @abc.abstractmethod
    def delete(self, url: str = '', **kwargs) -> Response:
        return super().delete(url=self.first_part_url + url, **kwargs)

