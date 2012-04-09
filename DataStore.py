import logging
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

from base import Base
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class DataStore:
	def __init__(self):
		#self.engine = create_engine('sqlite:///:memory:', echo=True)
		#self.engine = create_engine('sqlite:///:memory:')
		self.engine = create_engine('sqlite:///foo.db')
		logger.debug("Running on sqlachemy version %s" % (sqlalchemy.__version__))

		Session = sessionmaker(bind=self.engine)
		self.session = Session()

		Base.metadata.create_all(self.engine) 
		logger.debug("SQLAlchemy initialized")

	def add(self, obj):
		self.session.add(obj)

	def commit(self):
		self.session.commit()

