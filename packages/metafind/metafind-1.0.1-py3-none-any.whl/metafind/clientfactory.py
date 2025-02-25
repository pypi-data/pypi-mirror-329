from metafind.client import Client
from metafind.exifclient import ExifToolClient
from metafind.errors import UnsupportedBackend, BackendNotFound


from shutil import which


def get_client(backend: str, path: str) -> Client:
    """
    get_client returns a client for a metadata backend that has a standardized API for performing metadata analysis tasks.
    """
    if not _backend_exists(backend):
        raise BackendNotFound(backend)

    match backend:
        case "exiftool":
            return ExifToolClient(path)
        case _:
            raise UnsupportedBackend(backend)


def _backend_exists(backend: str):
    """
    backend_exists checks if the backend is on the host.

    Current implementation is naive, and assumes the provided name of the backend is the name of the tool on the system path.
    Should be more robust in the future, however this is the lowest amount of code implementation :)
    """
    if which(backend):
        return True
    return False
