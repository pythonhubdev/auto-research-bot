from contextlib import asynccontextmanager
from typing import Iterator

from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from auto_research_bot.config import settings

Base = declarative_base()


class Database:
    def __init__(self) -> None:
        self.url: str = settings.DATABASE_URL
        self.engine: Engine = create_engine(self.url, echo=settings.DEBUG)
        self.session = sessionmaker(self.engine)  # type: ignore

    @asynccontextmanager  # type: ignore
    def session(self) -> Iterator[Session]:
        session: Session = self.session()  # type: ignore
        try:
            yield session  # type: ignore
        except Exception:
            session.rollback()  # type: ignore
            raise
        finally:
            session.close()  # type: ignore

    @staticmethod
    def setup() -> None:
        config = Config("alembic.ini")
        command.upgrade(config, "head")
