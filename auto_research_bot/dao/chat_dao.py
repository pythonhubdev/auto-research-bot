from sqlalchemy import select

from auto_research_bot.database import ChatModel, Database


class ChatDAO:
    @staticmethod
    def create(chat_label: str) -> int:
        with Database().session() as session:  # type: ignore
            new_chat = ChatModel(chat_label=chat_label)
            session.add(new_chat)
            session.commit()
            return new_chat.id

    @staticmethod
    def get_all() -> list[ChatModel]:
        with Database().session() as session:  # type: ignore
            result = session.execute(select(ChatModel).order_by(ChatModel.created_at.desc()))
            chats = result.scalars().all()
            return chats
