from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSerializable
from langchain_openai import ChatOpenAI


class SummaryAgent:
    def __init__(self) -> None:
        self.openai: ChatOpenAI = ChatOpenAI(  # type: ignore
            model_name="gpt-3.5-turbo-1106",  # noqa
        )

    @staticmethod
    def summarize_prompt() -> PromptTemplate:
        template = """
        Hey, I need your help to create a concise summary of the structured information I have gathered.
        Please act as a SummarizationAgent and generate a well-written summary from the following key points:

        {key_points}

        The summary should be clear, informative, and capture the essence of the information provided.
        Thank you!
        """
        prompt = PromptTemplate(
            template=template,
            input_variables=["key_points"],
        )
        return prompt

    def llm(self) -> RunnableSerializable[dict[Any, Any], str]:
        llm: RunnableSerializable[dict[Any, Any], str] = (
            self.summarize_prompt()
            | self.openai
            | {
                "summary": StrOutputParser(),
            }
        )
        return llm
