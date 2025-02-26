"""Asynchronous Python client for Overseerr."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from importlib import metadata
import socket
from typing import TYPE_CHECKING, Any, Literal

from aiohttp import ClientError, ClientResponseError, ClientSession
from aiohttp.hdrs import METH_GET, METH_POST
from yarl import URL

from .exceptions import OverseerrAuthenticationError, OverseerrConnectionError
from .models import (
    Issue,
    IssueCount,
    IssueFilterStatus,
    IssueResponse,
    IssueSortStatus,
    MediaType,
    MovieDetails,
    NotificationType,
    RequestCount,
    RequestFilterStatus,
    RequestResponse,
    RequestSortStatus,
    RequestWithMedia,
    Result,
    SearchResult,
    Status,
    TVDetails,
    WatchlistEntry,
    WatchlistResponse,
    WebhookNotificationConfig,
)

if TYPE_CHECKING:
    from typing_extensions import Self


VERSION = metadata.version(__package__)


@dataclass
class OverseerrClient:
    """Main class for handling connections with Overseerr."""

    host: str
    port: int
    api_key: str
    ssl: bool = True
    session: ClientSession | None = None
    request_timeout: int = 10
    _close_session: bool = False

    async def _request(
        self,
        method: str,
        uri: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> str:
        """Handle a request to Overseerr."""
        url = URL.build(
            host=self.host, port=self.port, scheme="https" if self.ssl else "http"
        ).joinpath(f"api/v1/{uri}")

        headers = {
            "User-Agent": f"PythonOverseerr/{VERSION}",
            "Accept": "application/json",
            "X-Api-Key": self.api_key,
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    params=params,
                    headers=headers,
                    json=data,
                )
        except asyncio.TimeoutError as exception:
            msg = "Timeout occurred while connecting to the service"
            raise OverseerrConnectionError(msg) from exception
        except (
            ClientError,
            ClientResponseError,
            socket.gaierror,
        ) as exception:
            msg = "Error occurred while communicating with the service"
            raise OverseerrConnectionError(msg) from exception

        if response.status == 403:
            msg = "Invalid API key"
            raise OverseerrAuthenticationError(msg)

        if response.status >= 400:
            content_type = response.headers.get("Content-Type", "")
            text = await response.text()
            msg = "Unexpected response from Overseerr"
            raise OverseerrConnectionError(
                msg,
                {"Content-Type": content_type, "response": text},
            )

        return await response.text()

    async def get_request_count(self) -> RequestCount:
        """Get request count from Overseerr."""
        response = await self._request(METH_GET, "request/count")
        return RequestCount.from_json(response)

    async def get_issue_count(self) -> IssueCount:
        """Get issue count from Overseerr."""
        response = await self._request(METH_GET, "issue/count")
        return IssueCount.from_json(response)

    async def get_status(self) -> Status:
        """Get status from Overseerr."""
        response = await self._request(METH_GET, "status")
        return Status.from_json(response)

    async def search(self, keyword: str) -> list[Result]:
        """Search for media in Overseerr."""
        response = await self._request(METH_GET, "search", params={"query": keyword})
        return SearchResult.from_json(response).results

    async def get_webhook_notification_config(self) -> WebhookNotificationConfig:
        """Get webhook notification config from Overseerr."""
        response = await self._request(METH_GET, "settings/notifications/webhook")
        return WebhookNotificationConfig.from_json(response)

    async def get_requests(
        self,
        status: RequestFilterStatus | None = None,
        sort: RequestSortStatus | None = None,
        requested_by: int | None = None,
    ) -> list[RequestWithMedia]:
        """Get requests from Overseerr."""
        params: dict[str, Any] = {}
        if status:
            params["filter"] = status
        if sort:
            params["sort"] = sort
        if requested_by:
            params["requestedBy"] = requested_by
        response = await self._request(METH_GET, "request", params=params)
        return RequestResponse.from_json(response).results

    async def create_request(
        self,
        media_type: MediaType,
        tmdb_id: int,
        seasons: list[int] | Literal["all"] | None = None,
    ) -> RequestWithMedia:
        """Create a request in Overseerr."""
        data = {"mediaType": media_type, "mediaId": tmdb_id}
        if seasons:
            data["seasons"] = seasons
        response = await self._request(METH_POST, "request", data=data)
        return RequestWithMedia.from_json(response)

    async def get_issues(
        self,
        status: IssueFilterStatus | None = None,
        sort: IssueSortStatus | None = None,
        requested_by: int | None = None,
    ) -> list[Issue]:
        """Get issues from Overseerr."""
        params: dict[str, Any] = {}
        if status:
            params["filter"] = status
        if sort:
            params["sort"] = sort
        if requested_by:
            params["requestedBy"] = requested_by
        response = await self._request(METH_GET, "issue", params=params)
        return IssueResponse.from_json(response).results

    async def get_movie_details(self, identifier: int) -> MovieDetails:
        """Get movie details from Overseerr."""
        response = await self._request(METH_GET, f"movie/{identifier}")
        return MovieDetails.from_json(response)

    async def get_tv_details(self, identifier: int) -> TVDetails:
        """Get tv details from Overseerr."""
        response = await self._request(METH_GET, f"tv/{identifier}")
        return TVDetails.from_json(response)

    async def get_watchlist(self) -> list[WatchlistEntry]:
        """Get watchlist from Overseerr."""
        response = await self._request(METH_GET, "discover/watchlist")
        return WatchlistResponse.from_json(response).results

    async def test_webhook_notification_config(
        self, webhook_url: str, json_payload: str
    ) -> bool:
        """Test webhook notification config with Overseerr."""
        try:
            await self._request(
                METH_POST,
                "settings/notifications/webhook/test",
                data={
                    "enabled": True,
                    "types": NotificationType.REQUEST_PENDING_APPROVAL,
                    "options": {"webhookUrl": webhook_url, "jsonPayload": json_payload},
                },
            )
        except OverseerrConnectionError:
            return False
        return True

    async def set_webhook_notification_config(
        self,
        *,
        enabled: bool,
        types: NotificationType,
        webhook_url: str,
        json_payload: str,
    ) -> None:
        """Get webhook notification config from Overseerr."""
        await self._request(
            METH_POST,
            "settings/notifications/webhook",
            data={
                "enabled": enabled,
                "types": types,
                "options": {"webhookUrl": webhook_url, "jsonPayload": json_payload},
            },
        )

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The OverseerrClient object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()
