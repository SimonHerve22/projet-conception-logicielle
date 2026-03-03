-- Supprime les tables si elles existent déjà
DROP TABLE IF EXISTS favoris;
DROP TABLE IF EXISTS utilisateurs;
DROP TABLE IF EXISTS player_stats;

-- Table des utilisateurs
CREATE TABLE utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudo TEXT NOT NULL UNIQUE,
    hash_mdp TEXT NOT NULL    -- nouveau : hash du mot de passe
);

-- Table des favoris
CREATE TABLE favoris (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    team_name TEXT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES utilisateurs(id)
        ON DELETE CASCADE
);

-- Index pour améliorer les performances
CREATE INDEX idx_favoris_user_id ON favoris(user_id);

-- Table des statistiques des joueurs
CREATE TABLE player_stats (
    tournoi TEXT NOT NULL,
    equipe TEXT NOT NULL,
    name TEXT NOT NULL,
    games INTEGER NOT NULL,
    wins INTEGER NOT NULL,
    losses INTEGER NOT NULL,
    winrate REAL NOT NULL,
    kda REAL NOT NULL,
    kill_participation REAL NOT NULL,
    main_champion TEXT NOT NULL,
    PRIMARY KEY (name, tournoi)
);