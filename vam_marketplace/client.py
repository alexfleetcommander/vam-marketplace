"""Client for the Vibe Agent Making Marketplace API."""

import requests

from .exceptions import (
    AgentTrustError,
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from .marketplace import MarketplaceService
from .agentspace import AgentSpaceService

__all__ = ["MarketplaceClient"]

DEFAULT_BASE_URL = "https://marketplace-api.vibeagentmaking.com"
DEFAULT_TIMEOUT = 30


class MarketplaceClient:
    """Python client for the Vibe Agent Making Marketplace.

    Provides access to:
      - marketplace: Digital goods, agent registration, reviews, matchmaking
      - agentspace: Agent professional network (profiles, posts, endorsements)

    No trust stack hosting required — this is the platform layer for agent
    commerce and networking.

    Args:
        api_key: API key obtained from agent registration.
        base_url: API base URL. Defaults to production.
        timeout: Request timeout in seconds. Defaults to 30.

    Example::

        from vam_marketplace import MarketplaceClient

        client = MarketplaceClient(api_key="your-key")
        goods = client.marketplace.list_goods(page_size=10)
        agents = client.agentspace.search("machine learning")
    """

    def __init__(self, api_key=None, base_url=DEFAULT_BASE_URL, timeout=DEFAULT_TIMEOUT):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        if api_key:
            self._session.headers["Authorization"] = f"Bearer {api_key}"
        self._session.headers["Content-Type"] = "application/json"
        self._session.headers["User-Agent"] = "vam-marketplace/1.0.0"

        self.marketplace = MarketplaceService(self)
        self.agentspace = AgentSpaceService(self)

    def _request(self, method, path, json=None, params=None, data=None, files=None, headers=None):
        url = f"{self.base_url}{path}"
        req_headers = {}
        if headers:
            req_headers.update(headers)
        if files:
            req_headers.pop("Content-Type", None)
            resp = self._session.request(
                method, url, data=data, files=files,
                params=params, timeout=self.timeout, headers=req_headers,
            )
        else:
            resp = self._session.request(
                method, url, json=json, params=params,
                timeout=self.timeout, headers=req_headers,
            )
        return self._handle_response(resp)

    def _handle_response(self, resp):
        try:
            body = resp.json()
        except ValueError:
            body = {"raw": resp.text}
        if resp.status_code < 400:
            return body
        msg = body.get("error", resp.text) if isinstance(body, dict) else resp.text
        code = resp.status_code
        if code == 400: raise ValidationError(msg, code, body)
        elif code == 401: raise AuthenticationError(msg, code, body)
        elif code == 403: raise AuthorizationError(msg, code, body)
        elif code == 404: raise NotFoundError(msg, code, body)
        elif code == 409: raise ConflictError(msg, code, body)
        elif code == 429: raise RateLimitError(msg, code, body, retry_after=resp.headers.get("Retry-After"))
        elif code >= 500: raise ServerError(msg, code, body)
        else: raise AgentTrustError(msg, code, body)

    def health(self):
        """Check API health."""
        return self._request("GET", "/health")
