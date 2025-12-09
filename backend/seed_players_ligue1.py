import os
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://transfer_user:transfer_pass@db:5432/transfermarkt",
)

SQUADS = {
    "Paris Saint-Germain": [
        ("Gianluigi Donnarumma", "Goalkeeper"),
        ("Achraf Hakimi", "Defender"),
        ("Marquinhos", "Defender"),
        ("Milan Škriniar", "Defender"),
        ("Nuno Mendes", "Defender"),
        ("Manuel Ugarte", "Midfielder"),
        ("Vitinha", "Midfielder"),
        ("Fabián Ruiz", "Midfielder"),
        ("Ousmane Dembélé", "Forward"),
        ("Kylian Mbappé", "Forward"),
        ("Randal Kolo Muani", "Forward"),
    ],
    "Marseille": [
        ("Pau López", "Goalkeeper"),
        ("Jonathan Clauss", "Defender"),
        ("Chancel Mbemba", "Defender"),
        ("Samuel Gigot", "Defender"),
        ("Renan Lodi", "Defender"),
        ("Valentin Rongier", "Midfielder"),
        ("Jordan Veretout", "Midfielder"),
        ("Amine Harit", "Midfielder"),
        ("Ismaïla Sarr", "Forward"),
        ("Pierre-Emerick Aubameyang", "Forward"),
        ("Vitinha", "Forward"),
    ],
    "Lyon": [
        ("Anthony Lopes", "Goalkeeper"),
        ("Clinton Mata", "Defender"),
        ("Dejan Lovren", "Defender"),
        ("Jake O'Brien", "Defender"),
        ("Nicolás Tagliafico", "Defender"),
        ("Corentin Tolisso", "Midfielder"),
        ("Maxence Caqueret", "Midfielder"),
        ("Rayan Cherki", "Midfielder"),
        ("Ernest Nuamah", "Forward"),
        ("Alexandre Lacazette", "Forward"),
        ("Mama Baldé", "Forward"),
    ],
    "Monaco": [
        ("Philipp Köhn", "Goalkeeper"),
        ("Vanderson", "Defender"),
        ("Guillermo Maripán", "Defender"),
        ("Mohamed Camara", "Midfielder"),  # îl folosim în linia defensivă/mid
        ("Caio Henrique", "Defender"),
        ("Youssouf Fofana", "Midfielder"),
        ("Denis Zakaria", "Midfielder"),
        ("Aleksandr Golovin", "Midfielder"),
        ("Takumi Minamino", "Forward"),
        ("Wissam Ben Yedder", "Forward"),
        ("Breel Embolo", "Forward"),
    ],
    "Lille": [
        ("Lucas Chevalier", "Goalkeeper"),
        ("Bafodé Diakité", "Defender"),
        ("Leny Yoro", "Defender"),
        ("Alexsandro", "Defender"),
        ("Ismaily", "Defender"),
        ("Benjamin André", "Midfielder"),
        ("Nabil Bentaleb", "Midfielder"),
        ("Angel Gomes", "Midfielder"),
        ("Edon Zhegrova", "Forward"),
        ("Jonathan David", "Forward"),
        ("Rémy Cabella", "Forward"),
    ],
    "Nice": [
        ("Marcin Bułka", "Goalkeeper"),
        ("Youcef Atal", "Defender"),
        ("Jean-Clair Todibo", "Defender"),
        ("Dante", "Defender"),
        ("Melvin Bard", "Defender"),
        ("Youssouf Ndayishimiye", "Midfielder"),
        ("Khéphren Thuram", "Midfielder"),
        ("Morgan Sanson", "Midfielder"),
        ("Gaëtan Laborde", "Forward"),
        ("Terem Moffi", "Forward"),
        ("Sofiane Diop", "Forward"),
    ],
    "Rennes": [
        ("Steve Mandanda", "Goalkeeper"),
        ("Hamari Traoré", "Defender"),
        ("Warmed Omari", "Defender"),
        ("Arthur Theate", "Defender"),
        ("Adrien Truffert", "Defender"),
        ("Benjamin Bourigeaud", "Midfielder"),
        ("Enzo Le Fée", "Midfielder"),
        ("Baptiste Santamaria", "Midfielder"),
        ("Désiré Doué", "Forward"),
        ("Amine Gouiri", "Forward"),
        ("Arnaud Kalimuendo", "Forward"),
    ],
    "Lens": [
        ("Brice Samba", "Goalkeeper"),
        ("Przemysław Frankowski", "Defender"),
        ("Kevin Danso", "Defender"),
        ("Facundo Medina", "Defender"),
        ("Deiver Machado", "Defender"),
        ("Salis Abdul Samed", "Midfielder"),
        ("Andy Diouf", "Midfielder"),
        ("Angelo Fulgini", "Midfielder"),
        ("Florian Sotoca", "Forward"),
        ("Elye Wahi", "Forward"),
        ("Adrien Thomasson", "Forward"),
    ],
    "Nantes": [
        ("Alban Lafont", "Goalkeeper"),
        ("Fabien Centonze", "Defender"),
        ("Nicolas Pallois", "Defender"),
        ("Jean-Charles Castelletto", "Defender"),
        ("Quentin Merlin", "Defender"),
        ("Moussa Sissoko", "Midfielder"),
        ("Pedro Chirivella", "Midfielder"),
        ("Ludovic Blas", "Midfielder"),
        ("Mostafa Mohamed", "Forward"),
        ("Ignatius Ganago", "Forward"),
        ("Moses Simon", "Forward"),
    ],
    "Saint-Étienne": [
        ("Gautier Larsonneur", "Goalkeeper"),
        ("Yvann Maçon", "Defender"),
        ("Anthony Briançon", "Defender"),
        ("Lamine Fomba", "Midfielder"),  # îl folosim mai jos
        ("Niels Nkounkou", "Defender"),
        ("Thomas Monconduit", "Midfielder"),
        ("Aïmen Moueffek", "Midfielder"),
        ("Mathieu Cafaro", "Midfielder"),
        ("Irvin Cardona", "Forward"),
        ("Jean-Philippe Krasso", "Forward"),
        ("Wesley Saïd", "Forward"),
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
        # găsim clubul în tabela clubs
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
                (player_name, None, position_id, club_id, 5000000.00),
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Done seeding Ligue 1 players!")


if __name__ == "__main__":
    main()

