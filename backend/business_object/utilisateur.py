class Utilisateur:
    def __init__(self, pseudo: str):
        if not isinstance(pseudo, str):
            raise TypeError("Le pseudo doit être une chaîne de caractères")

        pseudo = pseudo.strip()

        if pseudo == "":
            raise ValueError("Le pseudo ne peut pas être vide")

        self.__pseudo = pseudo

    @property
    def pseudo(self) -> str:
        return self.__pseudo

    def __repr__(self) -> str:
        return f"Utilisateur(pseudo='{self.__pseudo}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Utilisateur):
            return False
        return self.__pseudo == other.__pseudo

    def __hash__(self) -> int:
        return hash(self.__pseudo)
