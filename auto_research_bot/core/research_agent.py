from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSerializable
from langchain_openai import ChatOpenAI

from auto_research_bot.service import MediaWikiService, NewsService
from auto_research_bot.utils import TextUtils


class ResearchAgent:
    def __init__(self) -> None:
        self.openai: ChatOpenAI = ChatOpenAI(  # type: ignore
            model_name="gpt-3.5-turbo-1106",  # noqa
        )

    @staticmethod
    async def gather_data(topic: str) -> dict[str, Any]:
        wiki_data = await MediaWikiService.fetch_topic(topic)
        news_data = await NewsService.fetch_topic(topic)
        if not wiki_data:
            wiki_data = "No data found."
        if not news_data:
            news_data = ["No data found."]
        return {
            "wikipedia": TextUtils.truncate_text(wiki_data, 7500),
            "news": TextUtils.truncate_text("\n".join(news_data), 7500),
            "topic": topic,
        }

    @staticmethod
    def structure_data_prompt() -> PromptTemplate:
        template = (
            "Hey, I am currently doing some research on certain topics. I want you to help me with it, "
            "so please act as a ResearchAgent and gather key points from the data I provide you, which I "
            "have obtained from different sources. The data is as follows:\n\n"
            "Wikipedia Data:\n"
            "{wikipedia}\n\n"
            "News Data:\n"
            "{news}\n\n"
            "Please structure the above data into key points. Also, please ignore irrelevant information and only focus"
            " on the topic at hand which is {topic}"
        )
        prompt = PromptTemplate(
            template=template,
            input_variables=["wikipedia", "news", "topic"],
            template_format="f-string",
        )
        return prompt

    def llm(self) -> RunnableSerializable[dict[Any, Any], str]:
        llm: RunnableSerializable[dict[Any, Any], str] = (
            self.structure_data_prompt()
            | self.openai
            | {
                "key_points": StrOutputParser(),
            }
        )
        return llm
