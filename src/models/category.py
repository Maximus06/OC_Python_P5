"""This module contains the class representing a category"""

from sqlalchemy import Column, Integer, String

# from sqlalchemy.orm import relationship

from .base import Base


class Category(Base):
    """Represents a category"""

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
        """Return a string representation of the class"""
        return f"<Category(name={self.name})>"

    def __str__(self):
        """Return the string name of the category"""
        return self.name
