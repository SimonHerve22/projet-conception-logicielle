import logging
import logging.config
import os

import yaml


def initialiser_logs(nom):
    """Initialiser les logs à partir du fichier de config"""

    # Création du dossier logs à la racine si non existant
    os.makedirs("logs", exist_ok=True)

    with open("logging_config.yml", encoding="utf-8") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)

    logger = logging.getLogger("frontLogger")

    logger.info("-" * 50)
    logger.info(f"Lancement {nom}                           ")
    logger.info("-" * 50)
