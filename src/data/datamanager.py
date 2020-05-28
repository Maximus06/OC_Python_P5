"""This module contains the DataManager Class"""

from random import choice, choices

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

from ..settings import DATABASE, CATEGORIES, ALIMENT_BY_CATEGORY,\
                       DUMMY_PRODUCTS
from ..models.base import Base
from ..models.aliment import Aliment, aliment_subtitute_relation
from ..models.store import Store
from ..models.category import Category
from ..settings import DATABASE as db

class DataManager:
    """This class is in charge of CRUD operations with the DataBase"""

    def __init__(self, reset=False):
        # self.engine = create_engine('mysql://maximus:decimus@localhost/openfood')
        self.engine = create_engine(self._get_connection())
        Session = sessionmaker(bind=self.engine)
        # create a new session
        self.session = Session()

        # create schema if necessary
        if reset:
            self.create_tables()
    
    def _get_connection(self):
        """Construct and return a string database connection."""

        url = f"{db.get('dialect')}{db.get('user')}:{db.get('password')}" \
              f"@{db.get('server')}/{db.get('base')}"
        return url


    def create_tables(self):
        """Generate or regenerate database schema"""

        Base.metadata.drop_all(self.engine)
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
        
        # aliments = self.session.query(Aliment).\
        #     filter(Aliment.categories.any(name=category)).all()

        aliments = self.session.query(Aliment).\
            filter(Aliment.categories.any(name=category)).\
            filter(Aliment.nutrition_score > 'a').\
            all()

        
        return aliments

    def get_substitute(self, category):
        """Return an Aliment object with a A score
        
        args:
            category: the category of the Aliment to substitute
        """       

        # query the aliment of this category with a A score
        aliments = self.session.query(Aliment).\
            filter(Aliment.categories.any(name=category)).\
            filter(Aliment.nutrition_score=='a').\
            all()

        print(f'\nNombre de substition possible de score A: {len(aliments)}')

        substitut = choice(aliments)        

        return substitut

    def get_saved_substitutes(self):
        """Return  a list of saved substitutes"""

        # substitutes = self.session.query(aliment_subtitute_relation).all()
        sql = 'SELECT * From v_aliment_substitute'
        substitutes = self.engine.execute(sql)

        return substitutes

    def save_substitute(self, aliment, substitute):
        """This method save the the substitute aliment
        
        Arg:
            - aliment : the Aliment object replaced
            - subsitute : the Aliment object which is the substitute
        """

        # add the substitute to the aliment substitutes collection
        aliment.substitutes.append(substitute)
        self.session.commit()

