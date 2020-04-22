"""This module contains the class representing an aliment"""

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base
from .store import Store

aliments_stores_relation = Table('aliments_stores', Base.metadata,
    Column('aliment_id', Integer, ForeignKey('aliments.id')),
    Column('store_id', Integer, ForeignKey('stores.id'))
)

class Aliment(Base):
    __tablename__ = 'aliments'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    url = Column(String(255))
    nutrition_score = Column(String(1))
    nova_group = Column(String(1))

    stores = relationship("Store", secondary=aliments_stores_relation)

    def __init__(self, name, url, score, nova, stores=[]):
        self.name = name
        self.url = url
        self.nutrition_score = score
        self.nova_group = nova
        self.stores = stores

    def __repr__(self):
        return f"<Aliment(name={self.name}, url={self.url}, score= \
            {self.nutrition_score}, nova={self.nova_group}, stores={self.stores})>"