import streamlit as st
from dotenv import load_dotenv

from auto_research_bot.core import LangchainInteractions
from auto_research_bot.database import Database
from auto_research_bot.pages.home_page import HomePage
from auto_research_bot.utils.logging import configure_logging

st.set_page_config(page_title="Automated Research and Report Generation", page_icon="📚", layout="centered")


@st.cache_resource
def init_app():
    load_dotenv()
    database = Database()
    database.setup()
    configure_logging()
    return LangchainInteractions()


langchain_interactions = init_app()


def main():
    home = HomePage()
    st.title("Automated Research and Report Generation")

    new_chat_label_key = f"new_chat_label_{st.session_state.get('new_chat_counter', 0)}"
    new_chat_label = st.text_input("Enter a label for the new chat:", key=new_chat_label_key)

    if st.button("New Chat"):
        home.handle_new_chat(new_chat_label)

    chats = home.get_all_chats()
    chat_options = {chat.id: f"{chat.chat_label} - {chat.created_at.strftime('%Y-%m-%d %H:%M:%S')}" for chat in chats}
    chat_id = st.selectbox("Select a chat:", options=chat_options.keys(), format_func=lambda x: chat_options[x])

    if chat_id:
        home.handle_chat_selection(chat_id, chats)

    if "chat_id" in st.session_state:
        home.display_chat_interface(langchain_interactions)
    else:
        st.write("Please create a new chat or select an existing chat.")


if __name__ == "__main__":
    main()
