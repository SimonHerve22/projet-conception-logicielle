-- Insertion des utilisateurs
INSERT INTO utilisateurs (pseudo) VALUES ('alice');
INSERT INTO utilisateurs (pseudo) VALUES ('bob');
INSERT INTO utilisateurs (pseudo) VALUES ('charlie');
INSERT INTO utilisateurs (pseudo) VALUES ('david');

-- Favoris LEC pour alice
INSERT INTO favoris (user_id, team_name)
VALUES (
    (SELECT id FROM utilisateurs WHERE pseudo = 'alice'),
    'G2 Esports'
);

INSERT INTO favoris (user_id, team_name)
VALUES (
    (SELECT id FROM utilisateurs WHERE pseudo = 'alice'),
    'Fnatic'
);

-- Favoris LEC pour bob
INSERT INTO favoris (user_id, team_name)
VALUES (
    (SELECT id FROM utilisateurs WHERE pseudo = 'bob'),
    'Karmine Corp'
);

INSERT INTO favoris (user_id, team_name)
VALUES (
    (SELECT id FROM utilisateurs WHERE pseudo = 'bob'),
    'Team Vitality'
);

-- Favoris LEC pour charlie
INSERT INTO favoris (user_id, team_name)
VALUES (
    (SELECT id FROM utilisateurs WHERE pseudo = 'charlie'),
    'MAD Lions KOI'
);

-- Favoris LEC pour david
INSERT INTO favoris (user_id, team_name)
VALUES (
    (SELECT id FROM utilisateurs WHERE pseudo = 'david'),
    'SK Gaming'
);
