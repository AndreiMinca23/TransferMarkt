import os
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://transfer_user:transfer_pass@db:5432/transfermarkt",
)

SQUADS = {
    "AC Milan": [
        ("Mike Maignan", "Goalkeeper"),
        ("Davide Calabria", "Defender"),
        ("Fikayo Tomori", "Defender"),
        ("Malick Thiaw", "Defender"),
        ("Theo Hernández", "Defender"),
        ("Ismaël Bennacer", "Midfielder"),
        ("Sandro Tonali", "Midfielder"),
        ("Ruben Loftus-Cheek", "Midfielder"),
        ("Christian Pulisic", "Forward"),
        ("Olivier Giroud", "Forward"),
        ("Rafael Leão", "Forward"),
    ],
    "Inter": [
        ("Yann Sommer", "Goalkeeper"),
        ("Denzel Dumfries", "Defender"),
        ("Stefan de Vrij", "Defender"),
        ("Alessandro Bastoni", "Defender"),
        ("Federico Dimarco", "Defender"),
        ("Nicolò Barella", "Midfielder"),
        ("Hakan Çalhanoğlu", "Midfielder"),
        ("Henrikh Mkhitaryan", "Midfielder"),
        ("Denzel Dumfries", "Defender"),
        ("Lautaro Martínez", "Forward"),
        ("Marcus Thuram", "Forward"),
    ],
    "Juventus": [
        ("Wojciech Szczęsny", "Goalkeeper"),
        ("Danilo", "Defender"),
        ("Gleison Bremer", "Defender"),
        ("Federico Gatti", "Defender"),
        ("Alex Sandro", "Defender"),
        ("Manuel Locatelli", "Midfielder"),
        ("Adrien Rabiot", "Midfielder"),
        ("Weston McKennie", "Midfielder"),
        ("Federico Chiesa", "Forward"),
        ("Dušan Vlahović", "Forward"),
        ("Arkadiusz Milik", "Forward"),
    ],
    "Napoli": [
        ("Alex Meret", "Goalkeeper"),
        ("Giovanni Di Lorenzo", "Defender"),
        ("Amir Rrahmani", "Defender"),
        ("Juan Jesus", "Defender"),
        ("Mário Rui", "Defender"),
        ("Stanislav Lobotka", "Midfielder"),
        ("Piotr Zieliński", "Midfielder"),
        ("André-Frank Zambo Anguissa", "Midfielder"),
        ("Matteo Politano", "Forward"),
        ("Victor Osimhen", "Forward"),
        ("Khvicha Kvaratskhelia", "Forward"),
    ],
    "Roma": [
        ("Rui Patrício", "Goalkeeper"),
        ("Rick Karsdorp", "Defender"),
        ("Gianluca Mancini", "Defender"),
        ("Chris Smalling", "Defender"),
        ("Leonardo Spinazzola", "Defender"),
        ("Bryan Cristante", "Midfielder"),
        ("Lorenzo Pellegrini", "Midfielder"),
        ("Houssem Aouar", "Midfielder"),
        ("Paulo Dybala", "Forward"),
        ("Tammy Abraham", "Forward"),
        ("Andrea Belotti", "Forward"),
    ],
    "Lazio": [
        ("Ivan Provedel", "Goalkeeper"),
        ("Manuel Lazzari", "Defender"),
        ("Nicolò Casale", "Defender"),
        ("Alessio Romagnoli", "Defender"),
        ("Adam Marušić", "Defender"),
        ("Danilo Cataldi", "Midfielder"),
        ("Luis Alberto", "Midfielder"),
        ("Sergej Milinković-Savić", "Midfielder"),
        ("Felipe Anderson", "Forward"),
        ("Ciro Immobile", "Forward"),
        ("Mattia Zaccagni", "Forward"),
    ],
    "Atalanta": [
        ("Juan Musso", "Goalkeeper"),
        ("Hans Hateboer", "Defender"),
        ("Rafael Tolói", "Defender"),
        ("Giorgio Scalvini", "Defender"),
        ("Joakim Mæhle", "Defender"),
        ("Marten de Roon", "Midfielder"),
        ("Teun Koopmeiners", "Midfielder"),
        ("Éderson", "Midfielder"),
        ("Ademola Lookman", "Forward"),
        ("Duván Zapata", "Forward"),
        ("Luis Muriel", "Forward"),
    ],
    "Fiorentina": [
        ("Pietro Terracciano", "Goalkeeper"),
        ("Dodô", "Defender"),
        ("Nikola Milenković", "Defender"),
        ("Lucas Martínez Quarta", "Defender"),
        ("Cristiano Biraghi", "Defender"),
        ("Rolando Mandragora", "Midfielder"),
        ("Giacomo Bonaventura", "Midfielder"),
        ("Arthur Melo", "Midfielder"),
        ("Nicolás González", "Forward"),
        ("Luka Jović", "Forward"),
        ("Jonathan Ikoné", "Forward"),
    ],
    "Torino": [
        ("Vanja Milinković-Savić", "Goalkeeper"),
        ("Wilfried Singo", "Defender"),
        ("Alessandro Buongiorno", "Defender"),
        ("Perr Schuurs", "Defender"),
        ("Mërgim Vojvoda", "Defender"),
        ("Samuele Ricci", "Midfielder"),
        ("Karol Linetty", "Midfielder"),
        ("Nemanja Radonjić", "Midfielder"),
        ("Nikola Vlašić", "Forward"),
        ("Antonio Sanabria", "Forward"),
        ("Pietro Pellegri", "Forward"),
    ],
    "Sassuolo": [
        ("Andrea Consigli", "Goalkeeper"),
        ("Jeremy Toljan", "Defender"),
        ("Gian Marco Ferrari", "Defender"),
        ("Martin Erlić", "Defender"),
        ("Rogério", "Defender"),
        ("Maxime López", "Midfielder"),
        ("Davide Frattesi", "Midfielder"),
        ("Hamed Traorè", "Midfielder"),
        ("Domenico Berardi", "Forward"),
        ("Andrea Pinamonti", "Forward"),
        ("Armand Laurienté", "Forward"),
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
        # căutăm clubul în tabela clubs
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
                (player_name, None, position_id, club_id, 7000000.00),
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Done seeding Serie A players!")


if __name__ == "__main__":
    main()
