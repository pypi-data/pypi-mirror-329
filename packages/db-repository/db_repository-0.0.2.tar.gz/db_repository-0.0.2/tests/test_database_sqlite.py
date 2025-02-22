import pytest
from db.database import create_db_session

# Define the DATABASE_URL for testing
DATABASE_URL = "sqlite+aiosqlite:///./test_database.db"

@pytest.mark.asyncio
async def test_db_connection():
    """Test database session creation."""
    # Create the session generator with the DATABASE_URL
    get_db = create_db_session(DATABASE_URL)

    # Use the session generator in the test
    async for db in get_db():
        assert db is not None
