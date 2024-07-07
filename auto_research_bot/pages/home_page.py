import asyncio

import streamlit as st
from loguru import logger
from streamlit import rerun

from auto_research_bot.core import LangchainInteractions
from auto_research_bot.dao import SummaryDAO
from auto_research_bot.dao.chat_dao import ChatDAO
from auto_research_bot.database import ChatModel, SummaryModel


class HomePage:
    @staticmethod
    def get_all_chats() -> list[ChatModel]:
        return ChatDAO.get_all()

    @staticmethod
    def create_new_chat(label: str) -> int:
        chat_id = ChatDAO.create(label)
        st.session_state.chat_id = chat_id
        st.session_state.chat_label = label
        st.session_state.topic = ""
        st.session_state.generated_summary = ""
        st.session_state.summaries = []
        st.session_state.summary_saved = False
        st.session_state.topic_disabled = False
        logger.info(f"New chat created: {chat_id}, {label}")
        return chat_id

    def handle_new_chat(self, label: str) -> None:
        if label:
            self.create_new_chat(label)
            st.session_state.new_chat_counter = st.session_state.get("new_chat_counter", 0) + 1
            rerun()
        else:
            st.error("Please enter a label for the new chat.")

    @staticmethod
    def generate_report(topic: str, langchain_interactions: LangchainInteractions) -> str:
        with st.spinner("Generating report..."):
            try:
                summary = asyncio.run(langchain_interactions.execute_research(topic))
                logger.info(f"Report generated for topic: {topic}")
                return summary
            except Exception as e:
                logger.error(f"Error generating report: {str(e)}")
                st.error("An error occurred while generating the report. Please try again.")
                return ""

    def handle_chat_selection(self, chat_id: int, chats: list[ChatModel]) -> None:
        if not st.session_state.get("chat_id") or st.session_state.chat_id != chat_id:
            st.session_state.chat_id = chat_id
            st.session_state.chat_label = next(chat.chat_label for chat in chats if chat.id == chat_id)
            summaries = SummaryDAO.get_all(chat_id)
            self.update_session_state_for_chat(summaries)
            logger.info(f"Chat selected: {chat_id}, {st.session_state.chat_label}")

    @staticmethod
    def update_session_state_for_chat(summaries: list[SummaryModel]) -> None:
        st.session_state.summaries = summaries
        st.session_state.summary_saved = bool(summaries)
        st.session_state.topic_disabled = bool(summaries)
        if summaries:
            st.session_state.generated_summary = summaries[-1].summary_text
            st.session_state.topic = summaries[-1].topic
        else:
            st.session_state.generated_summary = ""
            st.session_state.topic = ""

    @staticmethod
    def save_summary(chat_id: int, topic: str, summary: str) -> None:
        try:
            SummaryDAO.create(chat_id, topic, summary)
            st.success("Summary saved to the database.")
            st.session_state.summaries = SummaryDAO.get_all(chat_id)
            st.session_state.summary_saved = True
            st.session_state.topic_disabled = True
            st.session_state.generated_summary = summary  # Keep the summary
            rerun()
        except Exception as e:
            logger.error(f"Error saving summary: {str(e)}")
            st.error("An error occurred while saving the summary. Please try again.")

    @staticmethod
    def update_summary(summary_id: int, new_text: str) -> None:
        try:
            SummaryDAO.update(summary_id, new_text)
            st.success("Summary updated successfully.")
            st.session_state.summaries = SummaryDAO.get_all(st.session_state.chat_id)
            st.session_state.generated_summary = new_text  # Update the generated summary
            rerun()
        except Exception as e:
            logger.error(f"Error updating summary: {str(e)}")
            st.error("An error occurred while updating the summary. Please try again.")

    def display_summary_section(self, chat_id: int) -> None:
        if st.session_state.generated_summary and not st.session_state.summary_saved:
            st.header("Generated Summary")
            edited_summary = st.text_area(
                "Summary",
                st.session_state.generated_summary,
                height=300,
                key=f"generated_summary_{chat_id}",
            )
            if st.button("Save Summary", key=f"save_summary_{chat_id}"):
                self.save_summary(chat_id, st.session_state.topic, edited_summary)
        elif st.session_state.summaries:
            summary = st.session_state.summaries[-1]  # Get the most recent summary
            st.subheader(f"Topic: {summary.topic}")
            summary_input = st.text_area("", value=summary.summary_text, height=300, key=f"summary_{summary.id}")
            if st.button("Update Summary", key=f"update_summary_{summary.id}"):
                self.update_summary(summary.id, summary_input)

    def display_chat_interface(self, langchain_interactions: LangchainInteractions) -> None:
        chat_id = st.session_state.chat_id

        topic_input = st.text_input(
            "Enter a topic:",
            value=st.session_state.get("topic", ""),
            disabled=st.session_state.topic_disabled,
            key=f"topic_input_{chat_id}",
        )

        if not st.session_state.topic_disabled and st.button("Generate Report", key=f"generate_report_{chat_id}"):
            if topic_input:
                summary = self.generate_report(topic_input, langchain_interactions)
                st.session_state.topic = topic_input
                st.session_state.generated_summary = summary
                st.session_state.summary_saved = False

        self.display_summary_section(chat_id)
