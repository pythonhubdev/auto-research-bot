import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auto_research_bot.database import ChatModel
from auto_research_bot.database.connection import Base


class SummaryModel(Base):
    __tablename__ = "summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("chats.id"), nullable=False)
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now(datetime.UTC),
        nullable=False,
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime,
        onupdate=datetime.datetime.now(datetime.UTC),
    )
    chat: Mapped["ChatModel"] = relationship("ChatModel", back_populates="summaries")
