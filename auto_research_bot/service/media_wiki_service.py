from typing import Optional

from httpx import HTTPStatusError, RequestError
from loguru import logger

from auto_research_bot.service.httpx_service import HttpxService


class MediaWikiService:
    @staticmethod
    async def fetch_topic(topic: str) -> Optional[str]:
        async with HttpxService("https://en.wikipedia.org/w/api.php") as service:
            params = {
                "action": "query",
                "format": "json",
                "titles": topic,
                "prop": "revisions",
                "rvprop": "content",
                "rvslots": "main",
                "rvlimit": 1,
                "redirects": 1,
            }
            try:
                response = await service.get("", params=params)
                pages = response.get("query", {}).get("pages", {})
                for page_id, page in pages.items():
                    if page_id != "-1":
                        revisions = page.get("revisions", [])
                        if revisions:
                            return revisions[0].get("slots", {}).get("main", {}).get("*", "")
            except HTTPStatusError as exc:
                logger.error(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
                raise
            except RequestError as exc:
                logger.error(f"Request error occurred: {exc}")
                raise
        return None
