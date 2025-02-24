import os
from typing import Any, Optional, Union

import httpx
from httpx import URL, Timeout

from protean.models import cast_to_base_model


class ProteanService:
    client: httpx.Client

    def call(
            self,
            method: str,
            url: URL | str,
            json: Any | None = None,
            response_type: Any | None = None,
    ):
        try:
            response = self.client.request(
                method=method,
                url=url,
                json=json
            )

            # Raise the `HTTPStatusError` if one occurred.
            response.raise_for_status()

            if response_type is not None:
                return cast_to_base_model(response.text, response_type)

            return response

        except httpx.HTTPError as exception:
            raise exception
        finally:
            self.client.close()

    def __init__(self, client: httpx.Client):
        self.client = client


class ProteanServiceClient(httpx.Client):
    def default_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def __init__(
            self,
            *,
            api_key: Optional[str] = None,
            base_url: Union[str, URL, None] = None,
            timeout: Union[float, Timeout, None] = None
    ) -> None:
        if api_key is None:
            api_key = os.environ.get("PROTEAN_API_KEY")
        if api_key is None:
            raise ValueError(
                "The api_key client option must be set either by passing api_key to the client or by setting the PROTEAN_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("PROTEAN_BASE_URL")
        if base_url is None:
            raise ValueError(
                "The base_url client option must be set either by passing base_url to the client or by setting the PROTEAN_BASE_URL environment variable"
            )
        self.base_url = base_url

        super().__init__(
            base_url=base_url,
            timeout=timeout,
            headers=self.default_headers()
        )
