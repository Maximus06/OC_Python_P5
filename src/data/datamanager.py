"""This module contains the DataManager Class"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

from ..settings import DATABASE, CATEGORIES, ALIMENT_BY_CATEGORY,\
                       DUMMY_PRODUCTS
from ..models.base import Base
from ..models.aliment import Aliment
from ..models.store import Store
from ..models.category import Category

class DataManager:
    """This class is in charge of CRUD operations with the DataBase"""

    def __init__(self):
        self.engine = create_engine('mysql://maximus:decimus@localhost/openfood')
        Session = sessionmaker(bind=self.engine)
        # create a new session
        self.session = Session()

        # create schema if necessary
        self.create_tables()

    def create_tables(self):
        """Generate database schema"""        
        Base.metadata.create_all(self.engine)
    
    def create_categories(self, categories):
        """create the categories in the database from a list of category"""
        
        # create a list of Category object from the category list
        obj_categories = [Category(cate) for cate in categories]
        
        self.session.add_all(obj_categories)
        try:
            self.session.commit()
        except IntegrityError:
            # categories already exist: so ignore the exception
            self.session.rollback()
            
        
    
    def save_stores(self, stores):
        # create a list of Store object from the store set
        store_list = list(stores)
        obj_stores = [Store(store) for store in store_list]
        
        self.session.add_all(obj_stores)
        self.session.commit()

    def save_food(self, aliments):
        """This method"""
        # Replace the list of store string by a list of Store Object
        for aliment in aliments:
            obj_stores = []
            for store in aliment.stores:
                obj_store = self.get_obj_store(store)
                if obj_store == None:
                    print(f'Oups something went wrong with store: {store}')
                else:
                    obj_stores.append(obj_store)

            aliment.stores = obj_stores    

        self.session.add_all(aliments)
        self.session.commit()
        self.session.close()

    def get_obj_category(self, name):    
        """Return a Category object from the database"""    
        category = self.session.query(Category).filter(
            Category.name == name).first()
        return category

    def get_categories(self):    
        """Return a list of categories object from the database"""    
        categories = self.session.query(Category).all()
        return categories

    def get_obj_store(self, name):
        """Return a Store object from the database"""
        store = self.session.query(Store).filter(
            Store.name == name).first()
        return store

    def get_aliments_from_category(self, category):
        """Return a list of Aliment from the arg category"""
        
        aliments = self.session.query(Aliment).\
            filter(Aliment.categories.any(name=category)).all()
        
        return aliments
