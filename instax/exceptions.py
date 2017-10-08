"""Exceptions for use in client."""


class CommandTimedOutException(TimeoutError):
    """Raise this when a command has timed out."""


class ConnectError(Exception):
    """Raise this when a connect fails."""


class CommandError(Exception):
    """Raise this when a command fails."""
