"""This module contains the class representing an aliment"""

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

# Relation table between aliment and store
aliment_store_relation = Table(
    'aliment_store',
    Base.metadata,
    Column('aliment_id', Integer, ForeignKey('aliment.id'), primary_key=True),
    Column('store_id', Integer, ForeignKey('store.id'), primary_key=True),
)

# Relation table between aliment and category
aliment_category_relation = Table(
    'aliment_category',
    Base.metadata,
    Column('aliment_id', Integer, ForeignKey('aliment.id'), primary_key=True),
    Column(
        'category_id', Integer, ForeignKey('category.id'), primary_key=True
    ),
)

# Relation table between aliment and aliment.
# (in order to memorize substitute of aliment).
aliment_subtitute_relation = Table(
    'aliment_substitute',
    Base.metadata,
    Column('aliment_id', Integer, ForeignKey('aliment.id'), primary_key=True),
    Column(
        'substitute_id', Integer, ForeignKey('aliment.id'), primary_key=True
    ),
)


class Aliment(Base):
    __tablename__ = 'aliment'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    code_bar = Column(String(13))
    url = Column(String(255))
    nutrition_score = Column(String(1))
    nova_group = Column(String(1))
    brands = Column(String(100))

    stores = relationship("Store", secondary=aliment_store_relation)

    categories = relationship("Category", secondary=aliment_category_relation)

    substitutes = relationship(
        "Aliment",
        secondary=aliment_subtitute_relation,
        primaryjoin=id == aliment_subtitute_relation.c.aliment_id,
        secondaryjoin=id == aliment_subtitute_relation.c.substitute_id,
    )
    # foreign_keys=["aliment_id"])

    def __init__(
        self,
        name,
        description,
        code_bar,
        url,
        score,
        nova,
        brands,
        stores=[],
        categories=[],
        substitutes=[],
    ):
        self.name = name
        self.description = description
        self.code_bar = code_bar
        self.url = url
        self.nutrition_score = score
        self.nova_group = nova
        self.brands = brands
        self.stores = stores
        self.categories = categories
        self.substitutes = substitutes

    def __repr__(self):
        return f"<Aliment(name={self.name}, url={self.url}, score= \
            {self.nutrition_score}, nova={self.nova_group}, \
            stores={self.stores} categories={self.categories}, \
            substitutes={self.substitutes})>"

    def __eq__(self, aliment):
        """Return True if the code bar of two aliment are equal."""
        return self.code_bar == aliment.code_bar

    def get_stores(self):
        """Return a string of store with coma separator"""
        if self.stores is None:
            return ''

        str_store = ''
        for store in self.stores:
            str_store += f'{store.name}, '
        # remove the last ', '
        str_store = str_store[:-2]

        return str_store
