class MothMessageError(Exception):
    pass


class FailedToParseMessage(MothMessageError):
    pass


class UnknownMessageType(MothMessageError):
    pass
