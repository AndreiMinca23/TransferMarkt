import os
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://transfer_user:transfer_pass@db:5432/transfermarkt",
)

SQUADS = {
    "FCSB": [
        ("Ștefan Târnovanu", "Goalkeeper"),
        ("Valentin Crețu", "Defender"),
        ("Iulian Cristea", "Defender"),
        ("Joyskim Dawa", "Defender"),
        ("Radunović", "Defender"),
        ("Darius Olaru", "Midfielder"),
        ("Ovidiu Popescu", "Midfielder"),
        ("Adrian Șut", "Midfielder"),
        ("Octavian Popescu", "Forward"),
        ("Florinel Coman", "Forward"),
        ("Andrea Compagno", "Forward"),
    ],
    "CFR Cluj": [
        ("Cristian Bălgrădean", "Goalkeeper"),
        ("Cristian Manea", "Defender"),
        ("Andrei Burcă", "Defender"),
        ("Denis Kolinger", "Defender"),
        ("Camora", "Defender"),
        ("Ciprian Deac", "Midfielder"),
        ("Mihai Bordeianu", "Midfielder"),
        ("Jonathan Rodriguez", "Midfielder"),
        ("Cristian Manea", "Defender"),
        ("Billel Omrani", "Forward"),
        ("Daniel Bîrligea", "Forward"),
    ],
    "Universitatea Craiova": [
        ("Laurențiu Popescu", "Goalkeeper"),
        ("Vlad Chiricheș", "Defender"),
        ("Raul Silva", "Defender"),
        ("Bogdan Mitrea", "Defender"),
        ("Nicușor Bancu", "Defender"),
        ("Alexandru Crețu", "Midfielder"),
        ("Alexandru Cicâldău", "Midfielder"),
        ("Mihai Căpățînă", "Midfielder"),
        ("Andrei Ivan", "Forward"),
        ("Jovan Markovic", "Forward"),
        ("Elvir Koljić", "Forward"),
    ],
    "Rapid București": [
        ("Horatiu Moldovan", "Goalkeeper"),
        ("Răzvan Oaidă", "Defender"),
        ("Cristian Săpunaru", "Defender"),
        ("Paul Iacob", "Defender"),
        ("Junior Morais", "Defender"),
        ("Alexandru Albu", "Midfielder"),
        ("Dragoș Grigore", "Midfielder"),  # generic mid
        ("Damjan Djokovic", "Midfielder"),
        ("Antonio Sefer", "Forward"),
        ("Funsho Bamgboye", "Forward"),
        ("Marko Dugandžić", "Forward"),
    ],
    "Dinamo București": [
        ("Adnan Golubović", "Goalkeeper"),
        ("Denis Ciobotariu", "Defender"),
        ("Răzvan Patriche", "Defender"),
        ("Gabriel Moura", "Defender"),
        ("Vladimir Achim", "Defender"),  # generic
        ("Gorobsov", "Midfielder"),
        ("Paul Anton", "Midfielder"),
        ("Robert Moldoveanu", "Midfielder"),
        ("Deian Sorescu", "Forward"),
        ("Mattia Montini", "Forward"),
        ("Adam Nemec", "Forward"),
    ],
    "Farul Constanța": [
        ("Aioani", "Goalkeeper"),
        ("Romario Benzar", "Defender"),
        ("Ionuț Larie", "Defender"),
        ("Virgil Ghiță", "Defender"),
        ("Radu Boboc", "Defender"),
        ("Dragoș Nedelcu", "Midfielder"),
        ("Adrian Petre", "Midfielder"),  # generic mid
        ("Alexi Pitu", "Midfielder"),
        ("Louis Munteanu", "Forward"),
        ("Denis Alibec", "Forward"),
        ("Jefte Betancor", "Forward"),
    ],
    "Sepsi OSK": [
        ("Roland Niczuly", "Goalkeeper"),
        ("Radoslav Dimitrov", "Defender"),
        ("Bogdan Mitrea", "Defender"),
        ("Andres Dumitrescu", "Defender"),
        ("Mihai Bălașa", "Defender"),
        ("Jonathan Rodriguez", "Midfielder"),
        ("Păun", "Midfielder"),
        ("Adnan Aganović", "Midfielder"),
        ("Niczuly", "Midfielder"),  # generic
        ("Marius Ștefănescu", "Forward"),
        ("Mario Rondon", "Forward"),
    ],
    "UTA Arad": [
        ("Florin Iacob", "Goalkeeper"),
        ("Alexandru Benga", "Defender"),
        ("Erico da Silva", "Defender"),
        ("Shlyakov", "Defender"),
        ("Vlad Morar", "Defender"),  # generic
        ("Idriz Batha", "Midfielder"),
        ("Rareș Pop", "Midfielder"),
        ("Roger", "Midfielder"),
        ("David Miculescu", "Forward"),
        ("Filip Dangubić", "Forward"),
        ("Ioan Hora", "Forward"),
    ],
    "Petrolul Ploiești": [
        ("Marian Avram", "Goalkeeper"),
        ("Bart Meijers", "Defender"),
        ("Valentin Țicu", "Defender"),
        ("Ionuț Rada", "Defender"),
        ("Sergiu Hanca", "Defender"),
        ("Romario Moise", "Midfielder"),
        ("Patrick George", "Midfielder"),  # generic
        ("Mihai Roman", "Midfielder"),
        ("Gheorghe Grozav", "Forward"),
        ("Christian Irobiso", "Forward"),
        ("Babati", "Forward"),
    ],
    "Politehnica Iași": [
        ("Lukas Zima", "Goalkeeper"),
        ("Frăsinescu", "Defender"),
        ("Ionuț Panțîru", "Defender"),
        ("Mihalache", "Defender"),
        ("Rusu", "Defender"),
        ("Mihai Florescu", "Midfielder"),  # generici
        ("Ionuț Cioinac", "Midfielder"),
        ("Dylan Flores", "Midfielder"),
        ("Andrei Cristea", "Forward"),
        ("Platini", "Forward"),
        ("Mihai Roman II", "Forward"),
    ],
}


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # mapăm pozițiile după nume
    cur.execute("SELECT id, name FROM positions;")
    pos_rows = cur.fetchall()
    pos_by_name = {name: pid for pid, name in pos_rows}

    for club_name, players in SQUADS.items():
        cur.execute("SELECT id FROM clubs WHERE name = %s;", (club_name,))
        row = cur.fetchone()
        if not row:
            print(f"[WARN] Club not found in DB: {club_name}, skipping.")
            continue
        club_id = row[0]

        for player_name, position_name in players:
            position_id = pos_by_name.get(position_name)
            if not position_id:
                print(f"[WARN] Position not found: {position_name}, skipping {player_name}")
                continue

            print(f"Inserting {player_name} for {club_name}")
            cur.execute(
                """
                INSERT INTO players (name, nationality, position_id, current_club_id, market_value)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (player_name, None, position_id, club_id, 2000000.00),
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Done seeding SuperLiga players!")


if __name__ == "__main__":
    main()
