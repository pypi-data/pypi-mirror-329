import tempfile
import unittest
from pathlib import Path
from time import sleep

from sqlmodel import SQLModel, select

from commons.db import DatabaseAdapter, DatabaseMigrationExecutor

RESOURCES_FOLDER: Path = Path(__file__).parent / "resources"
TEMP_FOLDER: Path = Path(tempfile.gettempdir())


class TestDatabase(unittest.TestCase):
    @staticmethod
    def _get_db() -> DatabaseAdapter:
        return DatabaseAdapter(
            scheme="sqlite",
            database=tempfile.mktemp(dir=TEMP_FOLDER)
        )

    def test_database_creation(self):
        database: DatabaseAdapter = self._get_db()
        session = database.session()

        assert database
        assert database.engine()
        assert session
        session.close()

    def test_migration_files(self):
        from tests import TestUser

        db = self._get_db()
        SQLModel.metadata.create_all(db.engine())

        with db.session() as session:
            data = DatabaseMigrationExecutor(path=RESOURCES_FOLDER / "migrations", session=session).run()

            assert data
            assert session.exec(select(TestUser).where(TestUser.username == "john.doe")).first()
            assert session.exec(select(TestUser).where(TestUser.username == "joana.doe")).first()

            session.close()

    def test_cache(self):
        from commons.db.cache import Cache

        db = self._get_db()
        SQLModel.metadata.create_all(db.engine())

        with Cache(db) as cache:
            entry = cache.set("key", b"value", max_age=1)
            assert entry
            assert not entry.expired
            sleep(1)
            assert cache.get("key").expired

    async def test_async_db(self):
        import asyncio
        async def _inner_func():
            return self._get_db().engine()

        asyncio.run(_inner_func())

