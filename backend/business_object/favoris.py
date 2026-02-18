class Favoris:
    def __init__(self, pseudo: str, team_name: str):
        if not isinstance(pseudo, str):
            raise TypeError("Le pseudo doit être une chaîne de caractères")

        if not isinstance(team_name, str):
            raise TypeError("Le nom de l'équipe doit être une chaîne de caractères")

        pseudo = pseudo.strip()
        team_name = team_name.strip()

        if pseudo == "":
            raise ValueError("Le pseudo ne peut pas être vide")

        if team_name == "":
            raise ValueError("Le nom de l'équipe ne peut pas être vide")

        self.__pseudo = pseudo
        self.__team_name = team_name

    @property
    def pseudo(self) -> str:
        return self.__pseudo

    @property
    def team_name(self) -> str:
        return self.__team_name

    def __repr__(self) -> str:
        return f"Favoris(pseudo='{self.__pseudo}', team_name='{self.__team_name}')"
