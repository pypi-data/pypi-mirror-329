from typing import Union, Optional

from httpx import URL, Timeout

from ._base_classes import ProteanServiceClient
from .services import Chat, Vector


class Protean(ProteanServiceClient):
    chat: Chat
    vector: Vector

    def __init__(
            self,
            *,
            api_key: Optional[str] = None,
            base_url: Union[str, URL, None] = None,
            timeout: Union[float, Timeout, None] = None,
    ) -> None:
        self.chat = Chat(self)
        self.vector = Vector(self)

        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )
