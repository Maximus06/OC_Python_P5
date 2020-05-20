"""This module contains the class representing a category"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)    
    name = Column(String(100), nullable=False, unique=True)

    # aliments = relationship(
    #     "Aliment",
    #     secondary=aliments_category_relation,
    #     back_populates="category")

    def __init__(self, name):
        self.name = name    

    def __repr__(self):
        return f"<Category(name={self.name})>"