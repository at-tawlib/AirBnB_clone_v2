#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if not cls:
            return self.__objects
        elif type(cls) == str:
            return {key: value for key, value in
                    self.__objects.items() if value.__class__.__name__ == cls}
        else:
            return {key: value for key, value in
                    self.__objects.items() if value.__class__ == cls}

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as f:
            temp = {}
            for key in self.__objects:
                temp[key] = self.__objects[key].to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            temp = {}
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
            for k in temp:
                self.__objects[k] = classes[temp[k]['__class__']](**temp[k])
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete obj_from __objects if it's inside"""
        if obj is None:
            return
        else:
            del self.__objects[f"{obj.__class__.__name__}.{obj.id}"]
            self.save()

    def close(self):
        """call reload() for deserializing the JSON file to object"""
        self.reload()
