import datetime

from sqlalchemy import select

from auto_research_bot.database import Database, SummaryModel


class SummaryDAO:
    @staticmethod
    def create(chat_id: int, topic: str, summary_text: str) -> None:
        with Database().session() as session:  # type: ignore
            new_summary = SummaryModel(chat_id=chat_id, topic=topic, summary_text=summary_text)
            session.add(new_summary)
            session.commit()

    @staticmethod
    def update(summary_id: int, new_text: str) -> None:
        with Database().session() as session:  # type: ignore
            result = session.execute(
                select(SummaryModel).where(SummaryModel.id == summary_id),  # noqa
            )
            summary = result.scalar_one()
            summary.summary_text = new_text
            summary.updated_at = datetime.datetime.now(datetime.UTC)
            session.commit()

    @staticmethod
    def get_all(chat_id: int) -> list[SummaryModel]:
        with Database().session() as session:  # type: ignore
            result = session.execute(
                select(SummaryModel).where(SummaryModel.chat_id == chat_id).order_by(SummaryModel.created_at),  # noqa
            )
            summaries = result.scalars().all()
            return summaries
