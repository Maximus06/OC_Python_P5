from .aliment import Aliment
from .store import Store
from .base import Session, engine, Base

def create_base():
    # generate database schema
    Base.metadata.create_all(engine)

if __name__ == ('__main__'):
    create_base()
