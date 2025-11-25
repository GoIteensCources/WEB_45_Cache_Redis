import asyncio

from models.notes import Note
from settings import Base, async_engine, async_session


async def create_bd():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_data():
    async with async_session() as sess:
        n1 = Note(name="Make homework", description="theme 25")
        n2 = Note(name="go to shop", description="bread, milk")
        n3 = Note(name="cleaning", description="living room and kitchen")
        n4 = Note(name="call mom", description="ask about health")
        n5 = Note(name="read book", description="chapter 4 and 5")
        n6 = Note(name="exercise", description="30 minutes running")
        sess.add_all([n1, n2, n3, n4, n5, n6])
        await sess.commit()


async def main():
    await create_bd()
    print("database created")

    await insert_data()
    print("data inserted")


if __name__ == "__main__":
    asyncio.run(main())
