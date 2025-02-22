from requests import Response


class PendingResponse(Response):
    def __init__(self, response: Response | None, exception: Exception | None, request: "PendingRequest"):
        super().__init__()
        if response is not None:
            self.__dict__.update(response.__dict__)
        self.exception = exception
        self.pending_request = request

    def is_exception(self):
        return self.exception is not None

    def is_not_exception(self):
        return self.exception is None

    def is_valid(self):
        return self.is_not_exception() and self.status_code == 200

    def __bool__(self):
        return self.is_valid()

    def __repr__(self):
        if self.is_not_exception():
            if self.status_code == 200:
                return f"<PendingResponse [{self.status_code}]>"
            return f"<PendingResponse [{self.status_code}]: {self.content}>"
        return f"<PendingResponse: [{self.exception}]>"
