"""Module de connection à la base de données"""

import sqlite3

from utils.singleton import Singleton


class DBConnection(metaclass=Singleton):
    def __init__(self):
        """Ouverture de la connexion"""
        self.__connection = None

    @property
    def connection(self):
        if self.__connection is None:
            self.__connection = sqlite3.connect("database.db")
        return self.__connection

    def close(self):
        if self.__connection:
            self.__connection.close()
            self.__connection = None
