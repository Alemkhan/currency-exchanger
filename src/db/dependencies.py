from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from .session import async_session_factory


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        yield session
