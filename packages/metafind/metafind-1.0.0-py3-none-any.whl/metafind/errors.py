class MetafindError(Exception):
    """
    Base class for all metafind exceptions.
    """

    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code

    def __str__(self) -> str:
        return f"{self.message}, {self.error_code}"


class UnsupportedBackend(MetafindError):
    """
    Exception that's raised when an unsupported backend is specified.
    """

    ERROR_CODE = 1

    def __init__(self, backend: str):
        super().__init__(
            f"{backend} is not currently supported as a backend for metafind",
            self.ERROR_CODE,
        )


class BackendNotFound(MetafindError):
    """
    Exception that's raised when the specified backend could not be located on the host.
    """

    ERROR_CODE = 2

    def __init__(self, backend: str):
        super().__init__(f"{backend} could not be found", self.ERROR_CODE)
