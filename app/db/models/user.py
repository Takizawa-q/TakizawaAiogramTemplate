from dataclasses import dataclass
from ..base import Base
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, Text, DateTime, select, text
from sqlalchemy.sql.functions import count
from sqlalchemy.orm import sessionmaker

@dataclass
class UserDTO:
    user_id: int
    username: Optional[str]
    full_name: Optional[str]
    reg_date: datetime = datetime.now()

@dataclass
class RegIntervals:
    all: int
    day: int
    week: int
    month: int
class User(Base):
    __tablename__ = "user"
    
    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    username = Column(Text, nullable=None)
    full_name = Column(Text, nullable=True)
    reg_date = Column(DateTime, default=datetime.now())
    
    def __str__(self):
        return f"User: {self.user_id}, {self.username}, " \
            f"{self.full_name}"
            

async def add_user(user: User, session_maker: sessionmaker) -> None:
    
    async with session_maker() as session:
        async with session.begin():
            await session.merge(user)
            await session.commit()
            
async def get_all_users(session_maker: sessionmaker) -> list[UserDTO]:
    async with session_maker() as session:
        async with session.begin():
            result = (await session.execute(
                select(User)
            )).scalars().all()
            return [_get_user_from_db(user) for user in result]

async def get_count_users(session_maker: sessionmaker) -> RegIntervals:
    async with session_maker() as session:
        async with session.begin():
            intervals, values = [
                f"reg_date >= NOW() - '1 day'::INTERVAL",
                f"reg_date >= NOW() - '1 week'::INTERVAL",
                f"reg_date >= NOW() - '1 month'::INTERVAL",
            ], []

            count_users = (await session.execute(
                count(User.user_id)
            )).scalar_one()

            for interval in intervals:
                val = await session.execute(select(User.user_id).filter(text(interval)))
                values.append(len(val.scalars().all()))

            return RegIntervals(
                all=count_users,
                day=values[0],
                week=values[1],
                month=values[2]
            )

def _get_user_from_db(user: UserDTO) -> UserDTO:
    return UserDTO(
        user_id=user.user_id,
        username=user.username,
        full_name=user.full_name,
        reg_date=user.reg_date,
    )
    

