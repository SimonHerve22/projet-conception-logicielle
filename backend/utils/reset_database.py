import logging

from utils.log_decorator import log
from utils.singleton import Singleton
from dao.db_connection import DBConnection


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """

    @log
    def lancer(self):

        # Lecture des fichiers SQL

        with open("database/init_db.sql", encoding="utf-8") as f:
            init_db_as_string = f.read()

        with open("database/data_test_db.sql", encoding="utf-8") as f:
            data_test_db_as_string = f.read()

        try:
            # Ouvre la connexion à SQLite
            connection = DBConnection().connection

            # Avec SQLite on peut exécuter plusieurs instructions SQL d'un coup
            # grâce à executescript()
            connection.executescript(init_db_as_string)
            # connection.executescript(data_test_db_as_string)

            # Valide les modifications
            connection.commit()

        except Exception as e:
            logging.info(e)
            raise

        finally:
            # Ferme la connexion
            connection.close()

        return True


if __name__ == "__main__":
    print(ResetDatabase().lancer())