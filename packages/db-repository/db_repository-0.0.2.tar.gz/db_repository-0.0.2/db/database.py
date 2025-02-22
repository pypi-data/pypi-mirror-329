from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

def create_db_session(DATABASE_URL: str) -> AsyncGenerator[AsyncSession, None]:
    """
    Creates an AsyncSessionLocal sessionmaker for the given database URL.

    Args:
        DATABASE_URL (str): The database URL to connect to.

    Returns:
        AsyncGenerator[AsyncSession, None]: The asynchronous session generator.
    """
    engine = create_async_engine(DATABASE_URL, echo=True)

    AsyncSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async def get_db() -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSessionLocal() as session:
            yield session

    return get_db
