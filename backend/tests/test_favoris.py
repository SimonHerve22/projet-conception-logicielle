"""Tests pour la classe Favoris"""

from business_object.favoris import Favoris
import pytest


class TestFavoris:
    def test_favoris_init_succes(self):
        # GIVEN
        pseudo = "Alice"
        team = "TeamA"

        # WHEN
        favoris = Favoris(pseudo, team)

        # THEN
        assert favoris.pseudo == pseudo
        assert favoris.team_name == team

    @pytest.mark.parametrize(
        "pseudo, team, exception, msg",
        [
            (123, "TeamA", TypeError, "Le pseudo doit être une chaîne de caractères"),
            (
                "Alice",
                456,
                TypeError,
                "Le nom de l'équipe doit être une chaîne de caractères",
            ),
            ("   ", "TeamA", ValueError, "Le pseudo ne peut pas être vide"),
            ("Alice", "   ", ValueError, "Le nom de l'équipe ne peut pas être vide"),
        ],
    )
    def test_favoris_init_erreurs(self, pseudo, team, exception, msg):
        # WHEN / THEN
        with pytest.raises(exception, match=msg):
            Favoris(pseudo, team)

    def test_favoris_repr(self):
        # GIVEN
        favoris = Favoris("Bob", "TeamB")
        resultat_attendu = "Favoris(pseudo='Bob', team_name='TeamB')"

        # WHEN
        affichage = repr(favoris)

        # THEN
        assert affichage == resultat_attendu

    @pytest.mark.parametrize(
        "pseudo1, team1, pseudo2, team2, resultat_attendu",
        [
            ("Alice", "TeamA", "Alice", "TeamA", True),  # même pseudo + team
            ("Alice", "TeamA", "Alice", "TeamB", False),  # team différent
            ("Alice", "TeamA", "Bob", "TeamA", False),  # pseudo différent
        ],
    )
    def test_favoris_eq_et_hash(self, pseudo1, team1, pseudo2, team2, resultat_attendu):
        # GIVEN
        fav1 = Favoris(pseudo1, team1)
        fav2 = Favoris(pseudo2, team2)

        # WHEN / THEN
        # On définit l'égalité comme même pseudo ET team_name
        assert (
            (fav1.pseudo == fav2.pseudo) and (fav1.team_name == fav2.team_name)
        ) is resultat_attendu
        # hash basé sur le tuple (pseudo, team_name)
        assert (
            hash((fav1.pseudo, fav1.team_name)) == hash((fav2.pseudo, fav2.team_name))
        ) is resultat_attendu
