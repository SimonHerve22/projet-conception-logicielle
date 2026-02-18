-- Supprime les tables si elles existent déjà
DROP TABLE IF EXISTS favoris;
DROP TABLE IF EXISTS utilisateurs;

-- Table des utilisateurs
CREATE TABLE utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudo TEXT NOT NULL UNIQUE
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
