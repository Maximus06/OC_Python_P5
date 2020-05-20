"""This module contains the class representing a store"""

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Store(Base):
    """This class represents a store"""

    __tablename__ = 'store'

    id = Column(Integer, primary_key=True)    
    name = Column(String(100), nullable=False)
    # name = Column(String(100), nullable=False, unique=True)

    # aliments = relationship(
    #     "Aliment",
    #     secondary=aliments_store_relation,
    #     back_populates="store")

    def __init__(self, name):
        self.name = name    

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Store(name={self.name})>"