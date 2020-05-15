from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: refactor create url from settings and adapt in datamanager
engine = create_engine('mysql://maximus:decimus@localhost/openfood')
Session = sessionmaker(bind=engine)

Base = declarative_base()