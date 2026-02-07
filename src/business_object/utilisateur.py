class Utilisateur:
    def __init__(self, pseudo):
        if not isinstance(pseudo, str):
            raise TypeError("Le pseudo doit être une chaîne de caractères")

        pseudo = pseudo.strip()
        if pseudo == "":
            raise ValueError("Le pseudo ne peut pas être vide")

        self.pseudo = pseudo
