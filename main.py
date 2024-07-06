import asyncio

from dotenv import load_dotenv
from streamlit import (button, cache_resource, error, header, selectbox, session_state, set_page_config, spinner,
                       subheader, success, text_area, text_input, title, write)

from auto_research_bot.core import LangchainInteractions
from auto_research_bot.dao import SummaryDAO
from auto_research_bot.dao.chat_dao import ChatDAO
from auto_research_bot.database import Database

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


def main():
    langchain_interactions = LangchainInteractions()  # Initialize the LangchainInteractions class

    title("Automated Research and Report Generation")

    new_chat_label = text_input("Enter a label for the new chat:")

    if button("New Chat"):
        if new_chat_label:
            chat_id = ChatDAO.create(new_chat_label)
            session_state.chat_id = chat_id
            session_state.chat_label = new_chat_label
        else:
            error("Please enter a label for the new chat.")

    chats = ChatDAO.get_all()
    chat_options = {chat.id: f"{chat.chat_label} - {chat.created_at.strftime('%Y-%m-%d %H:%M:%S')}" for chat in chats}
    chat_id = selectbox("Select a chat:", options=chat_options.keys(), format_func=lambda x: chat_options[x])

    if chat_id and (not session_state.get("chat_id") or session_state.chat_id != chat_id):
        session_state.chat_id = chat_id
        session_state.chat_label = next(chat.chat_label for chat in chats if chat.id == chat_id)
        summaries = SummaryDAO.get_all(chat_id)
        session_state.generated_summary = summaries[-1].summary_text if summaries else ""
        session_state.topic = summaries[-1].topic if summaries else ""
        session_state.summaries = summaries

    if "chat_id" in session_state:
        chat_id = session_state.chat_id

        summaries = session_state.summaries
        topic_disabled = bool(summaries)

        topic_input = text_input(
            "Enter a topic:",
            value=session_state.topic,
            disabled=topic_disabled,
            key="topic_input",
        )

        if button("Generate Report") and not topic_disabled:
            if topic_input:
                with spinner("Generating report..."):
                    summary = asyncio.run(langchain_interactions.execute_research(topic_input))
                    session_state.generated_summary = summary
                    write("Generated Summary:")
                    text_area("Summary", summary, height=300, key="generated_summary")

                    if button("Save Summary"):
                        SummaryDAO.create(chat_id, topic_input, summary)
                        success("Summary saved to the database.")
                        session_state.topic = topic_input
                        session_state.summaries = SummaryDAO.get_all(chat_id)
            else:
                error("Please enter a topic to generate a report.")

        header("Generated Summary")

        if len(summaries) > 0:
            summary = summaries[0]
            subheader(f"Topic: {summary.topic}")
            summary_input = text_area("", value=summary.summary_text, height=300, key=f"summary_{summary.id}")
            if button("Update Summary", key=f"update_summary_{summary.id}"):
                SummaryDAO.update(summary.id, summary_input)
                success("Summary updated successfully.")
                session_state.summaries = SummaryDAO.get_all(chat_id)

    else:
        write("Please create a new chat or select an existing chat.")


if __name__ == "__main__":
    main()
