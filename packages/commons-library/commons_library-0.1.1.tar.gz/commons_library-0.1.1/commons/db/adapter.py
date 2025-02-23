from asyncio import Lock
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, SecretStr, Field, field_serializer, PrivateAttr
from sqlalchemy.engine.base import Engine
from sqlmodel import Session, create_engine


class SqlDatetimeAdapter:
    """
    Adapter inspired by `web.py` [1] after deprecation of default datetime adapters for SQLite on Python v3.12 [2].

    [1] [web.py PR !786]:
    https://github.com/webpy/webpy/pull/786
    [2] [Deprecate default (built-in) sqlite3 converters and adapters  - Python.org]:
    https://discuss.python.org/t/deprecate-default-built-in-sqlite3-converters-and-adapters/15781/16
    """

    @staticmethod
    def to_timestamp(date_time: datetime) -> str:
        """
        Convert a Python datetime.datetime into a timezone-naive ISO 8601 date string.

        >>> SqlDatetimeAdapter.to_timestamp(datetime(2024, 9, 10, 10, 10, 0, 12))
        "2024-09-10T10:10:0.000012"
        """
        return date_time.isoformat()

    @staticmethod
    def to_datetime(timestamp: bytes) -> datetime:
        """
        Convert an ISO 8601 formatted bytestring to a datetime.datetime object.

        >>> SqlDatetimeAdapter.to_datetime(b"2024-09-10T10:10:0.000012")
        datetime.datetime(2024, 9, 10, 10, 10, 0, 12)
        """
        return datetime.strptime(timestamp.decode("utf-8"), "%Y-%m-%dT%H:%M:%S.%f")


class DatabaseAdapter(BaseModel):
    """
    Thread-Safe SQLAlchemy-like URL connector adapter.

    This class provides a way to connect to a database using a URL.
    It supports various database drivers, including SQLite, PostgreSQL, and MySQL.
    """
    scheme: str
    username: str | None = None
    password: SecretStr | None = None
    host: str = ""
    port: int | None = None
    database: str = Field(serialization_alias="path", default="sqlite.db")
    query: str = ""

    _engine: Engine | None = PrivateAttr(default=None)

    @field_serializer("password")
    def dump_secret(self, v):
        if v:
            return v.get_secret_value()

    # to use a threading.Lock object with Pydantic, use Optional to annotate the type and use Field to initialize, and
    # allow the class to have arbitrary types
    # Source: https://stackoverflow.com/a/77151583
    # Docs:   https://docs.pydantic.dev/1.10/usage/model_config/
    # Licensed under CC BY-SA
    class Config:
        arbitrary_types_allowed = True

    lock: Lock = Field(exclude=True, default=Lock())
    # --- end of code snippet ---

    def uri(self) -> str:
        """
        Provide the URI of a SQL database. It does dump the database password as plain-text.
        """
        from pydantic_core import MultiHostUrl

        return MultiHostUrl.build(
            **self.model_dump(by_alias=True)
        ).unicode_string()

    async def _make_engine(self) -> Engine:
        engine: Engine
        async with self.lock:
            if self.scheme.startswith("sqlite"):
                import sqlite3

                sqlite3.register_adapter(datetime, SqlDatetimeAdapter.to_timestamp)
                sqlite3.register_converter("timestamp", SqlDatetimeAdapter.to_datetime)

                engine = create_engine(self.uri())

        return engine

    def engine(self) -> Engine:
        if not self._engine:
            import asyncio
            self._engine = asyncio.run(self._make_engine())

        return self._engine

    def session(self) -> Session:
        return Session(self.engine())
