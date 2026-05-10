import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from back.data.db_session import SqlAlchemyBase


class OrderModel(SqlAlchemyBase):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  
    address = Column(String(255), nullable=False)  
    date = Column(DateTime, nullable=False)
    weight = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'address': self.address,
            'date': self.date.strftime('%Y-%m-%d %H:%M') if self.date else None,
            'weight': self.weight,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }