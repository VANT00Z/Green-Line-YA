import datetime
import sqlalchemy
from back.data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class OrderModel(SqlAlchemyBase):
    __tablename__ = 'orders'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    adress = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(
        sqlalchemy.DateTime, nullable=True, default=datetime.datetime.now)
    weight = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.String, default="Active")

    user_id = Column(Integer, ForeignKey('users.id'))
    relationship('user')
