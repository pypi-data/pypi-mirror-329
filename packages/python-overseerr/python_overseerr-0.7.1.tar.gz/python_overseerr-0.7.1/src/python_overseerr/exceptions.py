"""Asynchronous Python client for Overseerr."""


class OverseerrError(Exception):
    """Generic exception."""


class OverseerrConnectionError(OverseerrError):
    """Overseerr connection exception."""


class OverseerrAuthenticationError(OverseerrError):
    """Overseerr authentication exception."""
