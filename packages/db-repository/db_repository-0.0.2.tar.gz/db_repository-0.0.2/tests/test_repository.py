import pytest
from db.repository import BaseRepository
from db.base import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import NoResultFound

# Define a test model
class TestModel(Base):
    __tablename__ = "test_models"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

@pytest.fixture()
def test_repository():
    """Fixture for creating a repository instance."""
    return BaseRepository(TestModel)

@pytest.mark.asyncio
async def test_create_and_get(test_db: AsyncSession, test_repository: BaseRepository):
    """Test creating and retrieving an object."""
    async with test_db.begin():  # Use transaction
        obj_data = {"id": 1, "name": "Test Object"}
        obj = await test_repository.create(test_db, obj_data)
        assert obj.id == 1
        assert obj.name == "Test Object"

        retrieved_obj = await test_repository.get(test_db, obj.id)
        assert retrieved_obj is not None
        assert retrieved_obj.id == obj.id
        assert retrieved_obj.name == obj.name

@pytest.mark.asyncio
async def test_get_all(test_db: AsyncSession, test_repository: BaseRepository):
    """Test 'get_all' method"""
    async with test_db.begin():  # Use transaction
        obj_data_1 = {"id": 1, "name": "Test Object 1"}
        obj_data_2 = {"id": 2, "name": "Test Object 2"}
        await test_repository.create(test_db, obj_data_1)
        await test_repository.create(test_db, obj_data_2)

        result = await test_repository.get_all(test_db)
        assert len(result) == 2
        assert result[0].name == "Test Object 1"
        assert result[1].name == "Test Object 2"

@pytest.mark.asyncio
async def test_create(test_db: AsyncSession, test_repository: BaseRepository):
    """Test 'create' method"""
    async with test_db.begin():  # Use transaction
        obj_data = {"id": 1, "name": "Test Object"}

        result = await test_repository.create(test_db, obj_data)
        assert result is not None
        assert result.id == 1
        assert result.name == "Test Object"

        db_obj = await test_repository.get(test_db, 1)
        assert db_obj is not None
        assert db_obj.name == "Test Object"

@pytest.mark.asyncio
async def test_update(test_db: AsyncSession, test_repository: BaseRepository):
    """Test 'update' method"""
    async with test_db.begin():  # Use transaction
        obj_data = {"id": 1, "name": "Test Object"}
        obj = await test_repository.create(test_db, obj_data)

        update_data = {"name": "Updated Object"}
        updated_obj = await test_repository.update(test_db, obj.id, update_data)
        assert updated_obj is not None
        assert updated_obj.name == "Updated Object"

        db_obj = await test_repository.get(test_db, obj.id)
        assert db_obj.name == "Updated Object"

@pytest.mark.asyncio
async def test_update_not_found(test_db: AsyncSession, test_repository: BaseRepository):
    """Test 'update' when object is not found"""
    update_data = {"name": "Updated Object"}
    
    # Try to update a non-existing object
    with pytest.raises(NoResultFound):
        async with test_db.begin():  # Use transaction
            await test_repository.update(test_db, 999, update_data)

@pytest.mark.asyncio
async def test_delete(test_db: AsyncSession, test_repository: BaseRepository):
    """Test deleting an object."""
    async with test_db.begin():  # Use transaction
        obj_data = {"id": 1, "name": "Test Object"}
        obj = await test_repository.create(test_db, obj_data)

        await test_repository.delete(test_db, obj.id)

        deleted_obj = await test_repository.get(test_db, obj.id)
        assert deleted_obj is None

@pytest.mark.asyncio
async def test_delete_not_found(test_db: AsyncSession, test_repository: BaseRepository):
    """Test 'delete' when object is not found"""
    async with test_db.begin():  # Use transaction
        await test_repository.delete(test_db, 999)  # No exception should be raised
