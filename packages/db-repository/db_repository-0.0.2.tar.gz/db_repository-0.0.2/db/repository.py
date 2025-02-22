from typing import Type, TypeVar, Generic, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from db.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> ModelType:
        result = await db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_all(self, db: AsyncSession) -> List[ModelType]:
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_data: dict) -> ModelType:
        obj = self.model(**obj_data)
        db.add(obj)
        await db.flush()
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, id: int, obj_data: dict) -> ModelType:
        obj = await self.get(db, id)
        if not obj:
            raise NoResultFound(f"{self.model.__name__} not found")

        for key, value in obj_data.items():
            setattr(obj, key, value)

        await db.flush()
        await db.refresh(obj)
        return obj

    async def delete(self, db: AsyncSession, id: int) -> None:
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.flush()
