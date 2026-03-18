-- ============================================================
-- ACTIVATION DES FOREIGN KEYS (SQLite)
-- ============================================================

PRAGMA foreign_keys = ON;

-- ============================================================
-- SUPPRESSION DES TABLES (ordre important avec FK)
-- ============================================================

DROP TABLE IF EXISTS favoris;
DROP TABLE IF EXISTS utilisateurs;
DROP TABLE IF EXISTS player_stats;
DROP TABLE IF EXISTS regular_season_standings;
DROP TABLE IF EXISTS playoff_results;
DROP TABLE IF EXISTS matches;


-- ============================================================
-- TABLE UTILISATEURS
-- ============================================================

CREATE TABLE utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudo TEXT NOT NULL UNIQUE,
    hash_mdp TEXT NOT NULL
);


-- ============================================================
-- TABLE FAVORIS
-- ============================================================

CREATE TABLE favoris (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    team_name TEXT NOT NULL,

    FOREIGN KEY (user_id)
        REFERENCES utilisateurs(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_favoris_user_id 
    ON favoris(user_id);


-- ============================================================
-- TABLE PLAYER STATS
-- ============================================================

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

CREATE INDEX idx_player_stats_tournoi 
    ON player_stats(tournoi);

CREATE INDEX idx_player_stats_equipe 
    ON player_stats(equipe);


-- ============================================================
-- TABLE REGULAR SEASON STANDINGS
-- ============================================================

CREATE TABLE regular_season_standings (
    tournoi TEXT NOT NULL,
    rang INTEGER NOT NULL,
    equipe TEXT NOT NULL,
    score TEXT NOT NULL,
    winrate REAL NOT NULL,
    streak TEXT NOT NULL,

    PRIMARY KEY (tournoi, rang)
);

CREATE INDEX idx_regular_season_tournoi 
    ON regular_season_standings(tournoi);

CREATE INDEX idx_regular_season_equipe 
    ON regular_season_standings(equipe);


-- ============================================================
-- TABLE PLAYOFF RESULTS
-- ============================================================

CREATE TABLE playoff_results (
    tournoi TEXT NOT NULL,
    place TEXT NOT NULL,
    qualification TEXT NOT NULL,
    equipe TEXT NOT NULL,

    PRIMARY KEY (tournoi, place)
);

CREATE INDEX idx_playoff_tournoi 
    ON playoff_results(tournoi);

CREATE INDEX idx_playoff_equipe 
    ON playoff_results(equipe);


-- ============================================================
-- TABLE MATCHES
-- ============================================================

CREATE TABLE matches (
    tournoi TEXT NOT NULL,
    date TEXT NOT NULL,
    patch TEXT NOT NULL,
    blue_team TEXT NOT NULL,
    red_team TEXT NOT NULL,
    winner TEXT NOT NULL,

    PRIMARY KEY (tournoi, date, blue_team, red_team)
);

CREATE INDEX idx_matches_tournoi 
    ON matches(tournoi);

CREATE INDEX idx_matches_winner 
    ON matches(winner);

CREATE INDEX idx_matches_teams 
    ON matches(blue_team, red_team);