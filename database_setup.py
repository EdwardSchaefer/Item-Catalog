import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name':self.name,
        }

class Guitar(Base):
    __tablename__ = 'guitar'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    body_material = Column(String(50), nullable=False)
    neck_material = Column(String(50), nullable=False)
    fingerboard_material = Column(String(50), nullable=False)
    frets = Column(String(2), nullable=False)
    strings = Column(String(2), nullable=False)
    scale_length = Column(String(8), nullable=False)
    pickups = Column(String(50), nullable=False)
    bridge = Column(String(50), nullable=False)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    brand = relationship(Brand)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'body_material': self.body_material,
            'neck_material': self.neck_material,
            'fingerboard_material': self.fingerboard_material,
            'frets': self.frets,
            'scale_length': self.scale_length,
            'pickups': self.pickups,
            'bridge': self.bridge,
        }

engine = create_engine('postgresql+psycopg2://catalog:test123@localhost:5432/guitars')

print "Database set up!"
Base.metadata.create_all(engine)
