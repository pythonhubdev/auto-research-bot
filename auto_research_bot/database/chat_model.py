from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auto_research_bot.database.connection import Base

if TYPE_CHECKING:
    from auto_research_bot.database.summary_model import SummaryModel


class ChatModel(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_label: Mapped[str] = mapped_column(Text(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC), nullable=False)
    summaries: Mapped["SummaryModel"] = relationship("SummaryModel", back_populates="chat")
