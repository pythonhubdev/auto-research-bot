from httpx import HTTPStatusError, RequestError
from loguru import logger

from auto_research_bot.config import settings
from auto_research_bot.service.httpx_service import HttpxService


class NewsService:
    @staticmethod
    async def fetch_topic(topic: str) -> list[str]:
        async with HttpxService(base_url="https://newsapi.org/v2/everything") as service:
            params = {"q": topic, "apiKey": settings.NEWS_API_KEY}
            try:
                response = await service.get("", params=params)
                articles = response.get("articles", [])
                return [article["description"] for article in articles if article.get("description")]
            except HTTPStatusError as exc:
                logger.error(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
                return []
            except RequestError as exc:
                logger.error(f"Request error occurred: {exc}")
                return []
