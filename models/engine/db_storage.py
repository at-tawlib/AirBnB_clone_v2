#!/usr/bin/python3
"""
Database storage
"""
from sqlalchemy import create_engine
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.place import place_amenity

classes = {"User": User, "State": State, "City": City,
           "Amenity": Amenity, "Place": Place, "Review": Review}


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Object initialization"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine(
                f"mysql+mysqldb://{user}:{password}@{host}/{db}")

    if getenv("HBNB_ENV") == "test":
        Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query all on the current database"""
        if not self.__session:
            self.reload()
        dct = {}
        if type(cls) == str:
            cls = classes.get(cls, None)
        if cls is None:
            for c in classes.values():
                objs = self.__session.query(c)
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dct[key] = obj
        else:
            objs = self.__session.query(cls)
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                dct[key] = obj
        return dct

    def new(self, obj):
        """Adds a new object"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def save(self):
        """saves  current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes an object"""
        if not self.__session:
            self.reload()
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables of dtabase"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """closes the working SQLAlchemy session"""
        self.__session.remove()
