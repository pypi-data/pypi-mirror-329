from datetime import datetime, timedelta

from pydantic import computed_field
from sqlmodel import SQLModel, Field, Session, select

from commons.db import DatabaseAdapter


class CacheEntry(SQLModel, table=True):
    id: str = Field(nullable=False, primary_key=True)
    data: bytes | None = Field(nullable=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    max_age: int = Field(default=300, nullable=False)

    @computed_field
    @property
    def expires(self) -> datetime:
        return self.created_at + timedelta(seconds=self.max_age)

    @computed_field
    @property
    def expired(self) -> bool:
        return bool(datetime.now() >= self.expires)


class Cache:
    def __init__(self, database: DatabaseAdapter):
        self.database = database
        self.session: Session | None = None

    def get(self, key: str) -> CacheEntry | None:
        return self.session.exec(select(CacheEntry).where(CacheEntry.id == key)).first()

    def set(self, key: str, value: bytes, max_age: int = 300) -> CacheEntry:
        entry: CacheEntry = self.get(key)

        if (entry and entry.expired) or (not entry):
            entry = CacheEntry(id=key, data=value, max_age=max_age)
            self.session.add(entry)
            self.session.commit()

        return entry

    def __enter__(self):
        self.session = self.database.session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.session = None
