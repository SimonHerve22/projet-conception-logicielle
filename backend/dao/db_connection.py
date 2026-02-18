"""Module de connection à la base de données"""

import sqlite3
from utils.singleton import Singleton

import logging
import re

class DBConnection(metaclass=Singleton):

    def __init__(self):
        """Ouverture de la connexion"""

        self.__connection = sqlite3.connect("database.db")

    @property
    def connection(self):
        return self.__connection