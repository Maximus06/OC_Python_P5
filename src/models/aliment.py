"""This module contains the class representing an aliment"""

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

# Relation table between aliments and stores
aliments_stores_relation = Table('aliments_stores', Base.metadata,
    Column('aliment_id', Integer, ForeignKey('aliments.id')),
    Column('store_id', Integer, ForeignKey('stores.id'))
)

# Relation table between aliments and categories
aliments_categories_relation = Table('aliments_categories', Base.metadata,
    Column('aliment_id', Integer, ForeignKey('aliments.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class Aliment(Base):
    __tablename__ = 'aliments'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    code_bar = Column(String(13))
    url = Column(String(255))
    nutrition_score = Column(String(1))
    nova_group = Column(String(1))
    brands = Column(String(100))

    stores = relationship(
        "Store",
        secondary=aliments_stores_relation)

    categories = relationship(
        "Category",
        secondary=aliments_categories_relation)
    
    def __init__(self, name, description, code_bar, url, score, nova, brands, stores=[], categories=[]):
        self.name = name
        self.description = description
        self.code_bar = code_bar
        self.url = url
        self.nutrition_score = score
        self.nova_group = nova
        self.brands = brands
        self.stores = stores
        self.categories = categories

    def __repr__(self):
        return f"<Aliment(name={self.name}, url={self.url}, score= \
            {self.nutrition_score}, nova={self.nova_group}, \
            stores={self.stores} categories={self.categories})>"
    
    def __eq__(self, aliment):
        """Return True if the code bar of two aliments are equal."""
        return self.code_bar == aliment.code_bar
    
    def get_stores(self):
        """Return a string of stores"""
        if self.stores == None:
            print('stores vide')
            return ''

        str_stores = ''
        for store in self.stores:
            str_stores += f'{store.name}, '
        str_stores = str_stores[:-2]

        return str_stores    

