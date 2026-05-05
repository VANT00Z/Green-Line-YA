import datetime
from back.data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship


class OrderModel(SqlAlchemyBase):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    adress = Column(String, nullable=True)
    date = Column(DateTime, nullable=True, default=datetime.datetime.now)
    weight = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    status = Column(String, default="Active")

    # user_id = Column(Integer, ForeignKey('users.id'))
    # relationship('user')
