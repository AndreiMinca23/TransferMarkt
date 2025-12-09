import os
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://transfer_user:transfer_pass@db:5432/transfermarkt",
)

clubs = [
    ("Arsenal", 1, 1),
    ("Manchester City", 1, 1),
    ("Liverpool", 1, 1),
    ("Manchester United", 1, 1),
    ("Chelsea", 1, 1),
    ("Tottenham Hotspur", 1, 1),
    ("Newcastle United", 1, 1),
    ("Aston Villa", 1, 1),
    ("West Ham United", 1, 1),
    ("Brighton & Hove Albion", 1, 1),

    ("Real Madrid", 2, 2),
    ("Barcelona", 2, 2),
    ("Atletico Madrid", 2, 2),
    ("Sevilla", 2, 2),
    ("Valencia", 2, 2),
    ("Real Sociedad", 2, 2),
    ("Villarreal", 2, 2),
    ("Real Betis", 2, 2),
    ("Athletic Bilbao", 2, 2),
    ("Celta Vigo", 2, 2),

    ("Bayern Munich", 3, 3),
    ("Borussia Dortmund", 3, 3),
    ("RB Leipzig", 3, 3),
    ("Bayer Leverkusen", 3, 3),
    ("Borussia Mönchengladbach", 3, 3),
    ("Eintracht Frankfurt", 3, 3),
    ("Wolfsburg", 3, 3),
    ("SC Freiburg", 3, 3),
    ("Union Berlin", 3, 3),
    ("VfB Stuttgart", 3, 3),

    ("AC Milan", 4, 4),
    ("Inter", 4, 4),
    ("Juventus", 4, 4),
    ("Napoli", 4, 4),
    ("Roma", 4, 4),
    ("Lazio", 4, 4),
    ("Atalanta", 4, 4),
    ("Fiorentina", 4, 4),
    ("Torino", 4, 4),
    ("Sassuolo", 4, 4),

    ("Paris Saint-Germain", 5, 5),
    ("Marseille", 5, 5),
    ("Lyon", 5, 5),
    ("Monaco", 5, 5),
    ("Lille", 5, 5),
    ("Nice", 5, 5),
    ("Rennes", 5, 5),
    ("Lens", 5, 5),
    ("Nantes", 5, 5),
    ("Saint-Étienne", 5, 5),

    ("Ajax", 6, 6),
    ("PSV Eindhoven", 6, 6),
    ("Feyenoord", 6, 6),
    ("AZ Alkmaar", 6, 6),
    ("FC Utrecht", 6, 6),
    ("Vitesse", 6, 6),
    ("Heerenveen", 6, 6),
    ("FC Twente", 6, 6),
    ("Groningen", 6, 6),
    ("Sparta Rotterdam", 6, 6),

    ("FCSB", 7, 7),
    ("CFR Cluj", 7, 7),
    ("Universitatea Craiova", 7, 7),
    ("Rapid București", 7, 7),
    ("Dinamo București", 7, 7),
    ("Farul Constanța", 7, 7),
    ("Sepsi OSK", 7, 7),
    ("UTA Arad", 7, 7),
    ("Petrolul Ploiești", 7, 7),
    ("Politehnica Iași", 7, 7),
]


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    for name, country_id, competition_id in clubs:
        print(f"Inserting {name}")
        cur.execute(
            """
            INSERT INTO clubs (name, country_id, competition_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (name) DO NOTHING;
            """,
            (name, country_id, competition_id),
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Done seeding!")


if __name__ == "__main__":
    main()
