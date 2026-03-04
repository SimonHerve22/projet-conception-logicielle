"""Implémentation des tests pour la classe Utilisateur"""

from business_object.utilisateur import Utilisateur
import pytest


class TestUtilisateur:
    def test_utilisateur_init_succes(self):
        # GIVEN
        pseudo = "Alice"
        hash_mdp = b"hash123"

        # WHEN
        utilisateur = Utilisateur(pseudo, hash_mdp)

        # THEN
        assert utilisateur.pseudo == pseudo
        assert utilisateur.hash_mdp == hash_mdp

    def test_utilisateur_init_pseudo_non_str(self):
        # GIVEN
        pseudo = 123
        hash_mdp = b"hash123"
        message_attendu = "Le pseudo doit être une chaîne de caractères"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            Utilisateur(pseudo, hash_mdp)

    def test_utilisateur_init_pseudo_vide(self):
        # GIVEN
        pseudo = "   "
        hash_mdp = b"hash123"
        message_attendu = "Le pseudo ne peut pas être vide"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            Utilisateur(pseudo, hash_mdp)

    def test_utilisateur_init_hash_invalide_type(self):
        # GIVEN
        pseudo = "Alice"
        hash_mdp = "hash123"
        message_attendu = "Le hash du mot de passe est requis et doit être en bytes"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            Utilisateur(pseudo, hash_mdp)

    def test_utilisateur_init_hash_vide(self):
        # GIVEN
        pseudo = "Alice"
        hash_mdp = b""
        message_attendu = "Le hash du mot de passe est requis et doit être en bytes"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            Utilisateur(pseudo, hash_mdp)

    def test_utilisateur_repr(self):
        # GIVEN
        utilisateur = Utilisateur("Bob", b"hash456")
        resultat_attendu = "Utilisateur(pseudo='Bob')"

        # WHEN
        affichage = repr(utilisateur)

        # THEN
        assert affichage == resultat_attendu

    @pytest.mark.parametrize(
        "pseudo1, hash1, pseudo2, hash2, resultat_attendu",
        [
            ("Alice", b"hash1", "Alice", b"hash2", True),  # même pseudo
            ("Alice", b"hash1", "Bob", b"hash1", False),  # pseudo différent
            ("Alice", b"hash1", "alice", b"hash1", False),  # sensible à la casse
        ],
    )
    def test_utilisateur_eq_et_hash(
        self, pseudo1, hash1, pseudo2, hash2, resultat_attendu
    ):
        # GIVEN
        user1 = Utilisateur(pseudo1, hash1)
        user2 = Utilisateur(pseudo2, hash2)

        # WHEN / THEN
        assert (user1 == user2) is resultat_attendu
        assert (hash(user1) == hash(user2)) is resultat_attendu

    def test_utilisateur_eq_type_different(self):
        # GIVEN
        utilisateur = Utilisateur("Alice", b"hash123")
        other = "Alice"

        # WHEN / THEN
        assert (utilisateur == other) is False
