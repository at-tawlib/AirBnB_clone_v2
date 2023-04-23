#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """User class, inherits from BaseModel & Base"""
    __tablename__ = 'users'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade="all, delete-orphan")
        reviews = relationship("Review", backref="user",
                               cascade="all, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
