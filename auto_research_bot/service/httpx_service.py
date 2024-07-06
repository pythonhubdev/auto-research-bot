from typing import Any, Optional

from auto_research_bot.repository import HTTPXRepository


class HttpxService(HTTPXRepository):
    async def get(
        self,
        url: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Any:
        response = await self._client.get(self._full_url(url), params=params, headers=headers)  # type: ignore
        response.raise_for_status()
        return response.json()

    async def post(
        self,
        url: str,
        data: Optional[dict[str, Any] | str] = None,
        json: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Any:
        response = await self._client.post(self._full_url(url), data=data, json=json, headers=headers)  # type: ignore
        response.raise_for_status()
        return response.json()

    async def put(
        self,
        url: str,
        data: Optional[dict[str, Any] | str] = None,
        json: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Any:
        response = await self._client.put(self._full_url(url), data=data, json=json, headers=headers)  # type: ignore
        response.raise_for_status()
        return response.json()

    async def delete(
        self,
        url: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Any:
        response = await self._client.delete(self._full_url(url), params=params, headers=headers)  # type: ignore
        response.raise_for_status()
        return response.json()

    def _full_url(self, path: str) -> str:
        return f"{self.base_url}{path}"
