#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
import models


class State(BaseModel, Base):
    """ State class """

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref='states',
                              cascade="all, delete")
    else:
        name = ''

    def __init__(self, *args, **kwargs):
        """initialize state"""
        super().__init__(*args, **kwargs)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """
            filestorage getter attribute that returns City instances
            state_id equals the current state
            """
            cities_values = models.storage.all("City").values()
            list_city = []
            for city in cities_values:
                if city.state_id == self.id:
                    list_city.append(city)
            return list_city
