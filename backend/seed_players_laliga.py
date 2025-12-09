import os
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://transfer_user:transfer_pass@db:5432/transfermarkt",
)

SQUADS = {
    "Real Madrid": [
        ("Thibaut Courtois", "Goalkeeper"),
        ("Dani Carvajal", "Defender"),
        ("Éder Militão", "Defender"),
        ("David Alaba", "Defender"),
        ("Ferland Mendy", "Defender"),
        ("Aurélien Tchouaméni", "Midfielder"),
        ("Toni Kroos", "Midfielder"),
        ("Luka Modrić", "Midfielder"),
        ("Federico Valverde", "Forward"),
        ("Vinícius Júnior", "Forward"),
        ("Rodrygo", "Forward"),
    ],
    "Barcelona": [
        ("Marc-André ter Stegen", "Goalkeeper"),
        ("Jules Koundé", "Defender"),
        ("Ronald Araújo", "Defender"),
        ("Andreas Christensen", "Defender"),
        ("Alejandro Balde", "Defender"),
        ("Frenkie de Jong", "Midfielder"),
        ("Pedri", "Midfielder"),
        ("Gavi", "Midfielder"),
        ("Raphinha", "Forward"),
        ("Robert Lewandowski", "Forward"),
        ("João Félix", "Forward"),
    ],
    "Atletico Madrid": [
        ("Jan Oblak", "Goalkeeper"),
        ("Nahuel Molina", "Defender"),
        ("José María Giménez", "Defender"),
        ("Mario Hermoso", "Defender"),
        ("Reinildo Mandava", "Defender"),
        ("Koke", "Midfielder"),
        ("Rodrigo De Paul", "Midfielder"),
        ("Saúl Ñíguez", "Midfielder"),
        ("Ángel Correa", "Forward"),
        ("Álvaro Morata", "Forward"),
        ("Antoine Griezmann", "Forward"),
    ],
    "Sevilla": [
        ("Yassine Bounou", "Goalkeeper"),
        ("Jesús Navas", "Defender"),
        ("Nemanja Gudelj", "Defender"),
        ("Loïc Badé", "Defender"),
        ("Marcos Acuña", "Defender"),
        ("Fernando", "Midfielder"),
        ("Ivan Rakitić", "Midfielder"),
        ("Joan Jordán", "Midfielder"),
        ("Lucas Ocampos", "Forward"),
        ("Youssef En-Nesyri", "Forward"),
        ("Erik Lamela", "Forward"),
    ],
    "Valencia": [
        ("Giorgi Mamardashvili", "Goalkeeper"),
        ("Thierry Correia", "Defender"),
        ("Gabriel Paulista", "Defender"),
        ("Mouctar Diakhaby", "Defender"),
        ("José Gayà", "Defender"),
        ("Hugo Guillamón", "Midfielder"),
        ("André Almeida", "Midfielder"),
        ("Javi Guerra", "Midfielder"),
        ("Sergi Canós", "Forward"),
        ("Hugo Duro", "Forward"),
        ("Samuel Lino", "Forward"),
    ],
    "Real Sociedad": [
        ("Álex Remiro", "Goalkeeper"),
        ("Hamari Traoré", "Defender"),
        ("Robin Le Normand", "Defender"),
        ("Igor Zubeldia", "Defender"),
        ("Aihen Muñoz", "Defender"),
        ("Martín Zubimendi", "Midfielder"),
        ("Mikel Merino", "Midfielder"),
        ("Brais Méndez", "Midfielder"),
        ("Takefusa Kubo", "Forward"),
        ("Mikel Oyarzabal", "Forward"),
        ("André Silva", "Forward"),
    ],
    "Villarreal": [
        ("Pepe Reina", "Goalkeeper"),
        ("Juan Foyth", "Defender"),
        ("Raúl Albiol", "Defender"),
        ("Jorge Cuenca", "Defender"),
        ("Alfonso Pedraza", "Defender"),
        ("Étienne Capoue", "Midfielder"),
        ("Dani Parejo", "Midfielder"),
        ("Álex Baena", "Midfielder"),
        ("Yeremy Pino", "Forward"),
        ("Gerard Moreno", "Forward"),
        ("Alexander Sørloth", "Forward"),
    ],
    "Real Betis": [
        ("Claudio Bravo", "Goalkeeper"),
        ("Youssouf Sabaly", "Defender"),
        ("Germán Pezzella", "Defender"),
        ("Luiz Felipe", "Defender"),
        ("Juan Miranda", "Defender"),
        ("Guido Rodríguez", "Midfielder"),
        ("William Carvalho", "Midfielder"),
        ("Nabil Fekir", "Midfielder"),
        ("Rodri", "Forward"),
        ("Borja Iglesias", "Forward"),
        ("Ayoze Pérez", "Forward"),
    ],
    "Athletic Bilbao": [
        ("Unai Simón", "Goalkeeper"),
        ("Óscar de Marcos", "Defender"),
        ("Yeray Álvarez", "Defender"),
        ("Iñigo Martínez", "Defender"),
        ("Yuri Berchiche", "Defender"),
        ("Mikel Vesga", "Midfielder"),
        ("Oihan Sancet", "Midfielder"),
        ("Iker Muniain", "Midfielder"),
        ("Nico Williams", "Forward"),
        ("Iñaki Williams", "Forward"),
        ("Gorka Guruzeta", "Forward"),
    ],
    "Celta Vigo": [
        ("Iván Villar", "Goalkeeper"),
        ("Óscar Mingueza", "Defender"),
        ("Joseph Aidoo", "Defender"),
        ("Unai Núñez", "Defender"),
        ("Manu Sánchez", "Defender"),
        ("Fran Beltrán", "Midfielder"),
        ("Luca de la Torre", "Midfielder"),
        ("Carles Pérez", "Midfielder"),
        ("Jonathan Bamba", "Forward"),
        ("Iago Aspas", "Forward"),
        ("Jørgen Strand Larsen", "Forward"),
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
                (player_name, None, position_id, club_id, 6000000.00),
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Done seeding La Liga players!")


if __name__ == "__main__":
    main()

