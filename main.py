import asyncio

from dotenv import load_dotenv
from loguru import logger
from streamlit import (
    button,
    cache_resource,
    error,
    header,
    selectbox,
    session_state,
    set_page_config,
    spinner,
    subheader,
    success,
    text_area,
    text_input,
    title,
    write,
    rerun,
)

from auto_research_bot.core import LangchainInteractions
from auto_research_bot.dao import SummaryDAO
from auto_research_bot.dao.chat_dao import ChatDAO
from auto_research_bot.database import Database
from auto_research_bot.utils.logging import configure_logging

set_page_config(
    page_title="Automated Research and Report Generation",
    page_icon="📚",
    layout="centered",
)


@cache_resource
def init_app():
    load_dotenv()
    database = Database()
    database.setup()
    return True


init_app()

configure_logging()
langchain_interactions = LangchainInteractions()  # Initialize the LangchainInteractions class


def main():
    title("Automated Research and Report Generation")

    new_chat_label_key = "new_chat_label_" + str(session_state.get("new_chat_counter", 0))
    new_chat_label = text_input("Enter a label for the new chat:", key=new_chat_label_key)

    if button("New Chat"):
        if new_chat_label:
            chat_id = ChatDAO.create(new_chat_label)
            session_state.chat_id = chat_id
            session_state.chat_label = new_chat_label
            session_state.topic = ""
            session_state.generated_summary = ""
            session_state.summaries = []
            session_state.summary_saved = False
            session_state.topic_disabled = False
            logger.info(f"New chat created: {chat_id}, {new_chat_label}")
            session_state.new_chat_counter = session_state.get("new_chat_counter", 0) + 1
            rerun()
        else:
            error("Please enter a label for the new chat.")

    chats = ChatDAO.get_all()
    chat_options = {chat.id: f"{chat.chat_label} - {chat.created_at.strftime('%Y-%m-%d %H:%M:%S')}" for chat in chats}
    chat_id = selectbox("Select a chat:", options=chat_options.keys(), format_func=lambda x: chat_options[x])

    if chat_id and (not session_state.get("chat_id") or session_state.chat_id != chat_id):
        session_state.chat_id = chat_id
        session_state.chat_label = next(chat.chat_label for chat in chats if chat.id == chat_id)
        summaries = SummaryDAO.get_all(chat_id)
        session_state.summaries = summaries
        session_state.summary_saved = False
        session_state.topic_disabled = False
        if summaries:
            session_state.generated_summary = summaries[-1].summary_text
            session_state.topic = summaries[-1].topic
            session_state.topic_disabled = True
        else:
            session_state.generated_summary = ""
            session_state.topic = ""
        logger.info(f"Chat selected: {chat_id}, {session_state.chat_label}")
    if "chat_id" in session_state:
        chat_id = session_state.chat_id

        topic_input = text_input(
            "Enter a topic:",
            value=session_state.get("topic", ""),
            disabled=session_state.topic_disabled,
            key=f"topic_input_{chat_id}",
        )

        if not session_state.topic_disabled and button("Generate Report", key=f"generate_report_{chat_id}"):
            if topic_input:
                with spinner("Generating report..."):
                    # Mocked summary text
                    summary = asyncio.run(langchain_interactions.execute_research(topic_input))
                    session_state.topic = topic_input
                    session_state.generated_summary = summary
                    session_state.summary_saved = False
                    logger.info(f"Report generated for topic: {topic_input}")
        if session_state.generated_summary and not session_state.summary_saved:
            header("Generated Summary")
            text_area("Summary", session_state.generated_summary, height=300, key=f"generated_summary_{chat_id}")
            if button("Save Summary", key=f"save_summary_{chat_id}"):
                logger.info(
                    f"Attempting to save summary: chat_id={chat_id}, topic={session_state.topic}",
                )
                SummaryDAO.create(chat_id, session_state.topic, session_state.generated_summary)
                success("Summary saved to the database.")
                session_state.summaries = SummaryDAO.get_all(chat_id)
                session_state.summary_saved = True
                session_state.generated_summary = ""  # Clear the generated summary after saving
                session_state.topic_disabled = True
                rerun()

        elif session_state.summary_saved and len(session_state.summaries) > 0:
            summary = session_state.summaries[0]
            subheader(f"Topic: {summary.topic}")
            summary_input = text_area("", value=summary.summary_text, height=300, key=f"summary_{summary.id}")
            if button("Update Summary", key=f"update_summary_{summary.id}"):
                logger.info(f"Attempting to update summary: id={summary.id}, new_text={summary_input}")
                SummaryDAO.update(summary.id, summary_input)
                success("Summary updated successfully.")
                session_state.summaries = SummaryDAO.get_all(chat_id)
                logger.info(f"Summary updated: {session_state.summaries}")

    else:
        write("Please create a new chat or select an existing chat.")


if __name__ == "__main__":
    main()
