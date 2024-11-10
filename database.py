from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import asyncio

DATABASE_URL = "mysql+aiomysql://root:@localhost/myself_bd"


class workwithbd:
    def __init__(self) -> None:
        self.engine = create_async_engine(DATABASE_URL, echo=True, future=True)

        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

        self.Base = declarative_base()

    async def get_reviews(self):
        async with self.async_session() as session:
            stmt = text("SELECT * FROM  reviews;")
            result = await session.execute(stmt, {"age_threshold": 30})
            rows = result.all()
            await session.commit()
            return rows

    async def post_reviews(self, review): 
        try:
            async with self.async_session() as session:
                stmt = text(
                    "INSERT INTO reviews (Surname, Name, Lastname, Phonenumber, Email, review) VALUES (:surname, :name, :lastname, :phonenumber, :email, :review);"
                )
                params = {
                    "surname": review.surname,
                    "name": review.name,
                    "lastname": review.lastname,
                    "phonenumber": review.phone,
                    "email": review.email,
                    "review": review.review,
                }
                result = await session.execute(stmt, params)
                await session.commit()

                return True
                # Подтверждаем транзакцию после успешного выполнения

        except SQLAlchemyError as e:
            print(f"Ошибка при выполнении операции INSERT: {e}")
            return False