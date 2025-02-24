__all__ = ['ExtractResponseError', 'RequestError']


class _BaseError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class ExtractResponseError(_BaseError):
    def __init__(self, message: str = 'Error while extracting response'):
        super().__init__(message)


class RequestError(_BaseError):
    def __init__(self, message: str = 'Error while making request'):
        super().__init__(message)
