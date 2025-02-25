from abc import ABC, abstractmethod


class Client(ABC):
    """
    Client is the base class that all metadata clients will inherent and implement.
    This is used to enable the support of additional backends, which will be injected at runtime into the caller classes.
    """

    @abstractmethod
    def get_metadata(self):
        pass

    @abstractmethod
    def scrub_metadata(self):
        pass

    @abstractmethod
    def get_unique_tags(self):
        pass
