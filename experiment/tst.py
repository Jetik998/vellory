# import asyncio
#
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
#
#
#
#
# class Base(AsyncAttrs, DeclarativeBase):
#     pass
#
# class User(Base):
#     __tablename__ = 'user'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column()
#     age: Mapped[int] = mapped_column()
#
#     def __repr__(self) -> str:
#         return f"User(id={self.id}, name='{self.name}', age={self.age})"
#
# async def add_user(session, name:str, age:int):
#     user = User(name=name, age=age)
#     session.add(user)
#     await session.commit()
#
# async def get_all_users(session):
#     result = await session.execute(select(User))
#     return result.scalars().all()
#
# async def update_user_age(session, name: str, new_age: int):
#     result = await session.execute(select(User).where(User.name == name))
#     user = result.scalars().first()
#     if user:
#         user.age = new_age
#         await session.commit()
#
# async def delete_user(session, name: str):
#     result = await session.execute(select(User).where(User.name == name))
#     user = result.scalars().first()
#     if user:
#         await session.delete(user)
#         await session.commit()
#
#
# async def main():
#     engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
#     async_session = async_sessionmaker(engine, expire_on_commit=False)
#
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#     async with async_session() as session:
#         try:
#             await add_user(session, "Alice", 25)
#             await add_user(session, "Bob", 30)
#             await add_user(session, "Charlie", 22)
#             await update_user_age(session, "Alice", 26)
#             await delete_user(session, "Bob")
#             users = await get_all_users(session)
#             print(users)
#         except Exception as e:
#             print(e)
#
# asyncio.run(main())
