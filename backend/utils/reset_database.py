import os
import logging

from utils.log_decorator import log
from utils.singleton import Singleton
from backend.dao.db_connection import DBConnection


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """

    @log
    def lancer(self, test_dao=False):

        init_db = open("database/init_db.sql", encoding="utf-8")
        init_db_as_string = init_db.read()
        init_db.close()

        data_test_db = open("database/data_test_db.sql", encoding="utf-8")
        data_test_db_as_string = data_test_db.read()
        data_test_db.close()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(init_db_as_string)
                    cursor.execute(data_test_db_as_string)
        except Exception as e:
            logging.info(e)
            raise

        return True


if __name__ == "__main__":
    print(ResetDatabase().lancer())