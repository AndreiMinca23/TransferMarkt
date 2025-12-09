CREATE TABLE IF NOT EXISTS positions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS clubs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birth_date DATE,
    nationality VARCHAR(50),
    position_id INT REFERENCES positions(id),
    current_club_id INT REFERENCES clubs(id),
    market_value NUMERIC(12, 2)
);

CREATE TABLE IF NOT EXISTS transfers (
    id SERIAL PRIMARY KEY,
    player_id INT NOT NULL REFERENCES players(id),
    from_club_id INT REFERENCES clubs(id),
    to_club_id INT REFERENCES clubs(id),
    fee NUMERIC(12, 2),
    transfer_date DATE NOT NULL
);

INSERT INTO positions (name) VALUES
    ('Goalkeeper'),
    ('Defender'),
    ('Midfielder'),
    ('Forward')


ON CONFLICT (name) DO NOTHING;