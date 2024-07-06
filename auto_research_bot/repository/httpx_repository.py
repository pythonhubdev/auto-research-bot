from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

from httpx import AsyncClient


class HTTPXRepository(ABC):
    def __init__(self, base_url: str = "") -> None:
        self.base_url = base_url
        self._client: Optional[AsyncClient] = None

    async def __aenter__(self) -> "HTTPXRepository":
        self._client = AsyncClient()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._client:
            await self._client.aclose()

    @abstractmethod
    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        pass

    @abstractmethod
    async def post(
        self,
        url: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        pass

    @abstractmethod
    async def put(
        self,
        url: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        pass

    @abstractmethod
    async def delete(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        pass
