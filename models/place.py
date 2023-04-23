#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.sql.schema import Table
from os import getenv
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from models.review import Review

if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id',
                                 String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id',
                                 String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True,
                                 nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = 'places'

    if getenv('HBNB_TYPE_STORAGE') == 'db':

        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        reviews = relationship("Review", cascade="all, delete-orphan",
                               backref="place")
        amenities = relationship("Amenity",
                                 secondary='place_amenity',
                                 viewonly=False,
                                 backref="place_amenities")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """getter attribute in case of file storage"""
            review_lst = []
            if review in models.storage.all(Review):
                if review.place_id == self.id:
                    review_lst.append(review)
            return review_lst

        @property
        def amenities(self):
            """attribute that returns list of Amenity instances"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, instance=None):
            """Setter for the amenities property"""
            if type(instance) is Amenity:
                if instance.place_amenity.place_id == self.id:
                    self.amenity_ids.append(instance.id)
