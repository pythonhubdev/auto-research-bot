from typing import Any

from langchain_core.runnables.utils import Output
from loguru import logger
from openai import InternalServerError, RateLimitError

from auto_research_bot.core.research_agent import ResearchAgent
from auto_research_bot.core.summary_agent import SummaryAgent


class LangchainInteractions:
    def __init__(self) -> None:
        self.research_agent = ResearchAgent()
        self.summary_agent = SummaryAgent()

    async def execute_research(self, topic: str) -> Any:
        try:
            data = await self.research_agent.gather_data(topic)
            llm_chain = self.research_agent.llm() | self.summary_agent.llm()
            response: Output = await llm_chain.ainvoke(data)  # type: ignore
            summary = response["summary"]  # type: ignore
            return summary
        except (RateLimitError, InternalServerError) as exception:
            logger.error(f"Error while gathering data: {exception}")
            return {
                "error": "An error occurred while gathering data. Please try again later.",
                "details": f"{exception}",
            }
