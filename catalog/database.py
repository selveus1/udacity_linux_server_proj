
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import datetime


Base = declarative_base()


class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key = True)
	name =Column(String(80), nullable = False)
	email=Column(String(80), nullable = False)
	picture=Column(String(300))
	


class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	picture=Column(String(500))

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'name'         : self.name,
			'id'           : self.id,
		}


class Item(Base):
	__tablename__ = 'item'

	name =Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	description = Column(String(500))
	# date_added = Column(DateTime, default=datetime.datetime.utcnow)
	date_added = Column(String, default=datetime.datetime.utcnow().strftime("%A, %B %d %Y"))
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)
	
	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'name'         : self.name,
			'description'  : self.description,
			'id'           : self.id,
			'date_added'   : self.date_added,
		}


engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(engine)
