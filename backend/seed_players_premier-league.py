import os
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://transfer_user:transfer_pass@db:5432/transfermarkt",
)

# map club -> list de (nume jucator, pozitie)
# pozitia trebuie sa fie "Goalkeeper", "Defender", "Midfielder" sau "Forward"
# ca sa se potriveasca cu tabela positions.
SQUADS = {
    "Arsenal": [
        ("Aaron Ramsdale", "Goalkeeper"),
        ("Ben White", "Defender"),
        ("William Saliba", "Defender"),
        ("Gabriel Magalhães", "Defender"),
        ("Oleksandr Zinchenko", "Defender"),
        ("Declan Rice", "Midfielder"),
        ("Martin Ødegaard", "Midfielder"),
        ("Kai Havertz", "Midfielder"),
        ("Bukayo Saka", "Forward"),
        ("Gabriel Jesus", "Forward"),
        ("Gabriel Martinelli", "Forward"),
    ],
    "Manchester City": [
        ("Ederson", "Goalkeeper"),
        ("Kyle Walker", "Defender"),
        ("Rúben Dias", "Defender"),
        ("Nathan Aké", "Defender"),
        ("Joško Gvardiol", "Defender"),
        ("Rodri", "Midfielder"),
        ("Kevin De Bruyne", "Midfielder"),
        ("Bernardo Silva", "Midfielder"),
        ("Phil Foden", "Forward"),
        ("Erling Haaland", "Forward"),
        ("Julián Álvarez", "Forward"),
    ],
    "Liverpool": [
        ("Alisson", "Goalkeeper"),
        ("Trent Alexander-Arnold", "Defender"),
        ("Virgil van Dijk", "Defender"),
        ("Ibrahima Konaté", "Defender"),
        ("Andrew Robertson", "Defender"),
        ("Alexis Mac Allister", "Midfielder"),
        ("Dominik Szoboszlai", "Midfielder"),
        ("Curtis Jones", "Midfielder"),
        ("Mohamed Salah", "Forward"),
        ("Darwin Núñez", "Forward"),
        ("Luis Díaz", "Forward"),
    ],
    "Manchester United": [
        ("André Onana", "Goalkeeper"),
        ("Diogo Dalot", "Defender"),
        ("Raphaël Varane", "Defender"),
        ("Lisandro Martínez", "Defender"),
        ("Luke Shaw", "Defender"),
        ("Casemiro", "Midfielder"),
        ("Bruno Fernandes", "Midfielder"),
        ("Mason Mount", "Midfielder"),
        ("Antony", "Forward"),
        ("Rasmus Højlund", "Forward"),
        ("Marcus Rashford", "Forward"),
    ],
    "Chelsea": [
        ("Robert Sánchez", "Goalkeeper"),
        ("Reece James", "Defender"),
        ("Thiago Silva", "Defender"),
        ("Axel Disasi", "Defender"),
        ("Ben Chilwell", "Defender"),
        ("Enzo Fernández", "Midfielder"),
        ("Moises Caicedo", "Midfielder"),
        ("Conor Gallagher", "Midfielder"),
        ("Raheem Sterling", "Forward"),
        ("Nicolas Jackson", "Forward"),
        ("Mykhailo Mudryk", "Forward"),
    ],
    "Tottenham Hotspur": [
        ("Guglielmo Vicario", "Goalkeeper"),
        ("Pedro Porro", "Defender"),
        ("Cristian Romero", "Defender"),
        ("Micky van de Ven", "Defender"),
        ("Destiny Udogie", "Defender"),
        ("Yves Bissouma", "Midfielder"),
        ("James Maddison", "Midfielder"),
        ("Pape Matar Sarr", "Midfielder"),
        ("Dejan Kulusevski", "Forward"),
        ("Heung-min Son", "Forward"),
        ("Richarlison", "Forward"),
    ],
    "Newcastle United": [
        ("Nick Pope", "Goalkeeper"),
        ("Kieran Trippier", "Defender"),
        ("Fabian Schär", "Defender"),
        ("Sven Botman", "Defender"),
        ("Dan Burn", "Defender"),
        ("Bruno Guimarães", "Midfielder"),
        ("Joelinton", "Midfielder"),
        ("Sandro Tonali", "Midfielder"),
        ("Miguel Almirón", "Forward"),
        ("Alexander Isak", "Forward"),
        ("Anthony Gordon", "Forward"),
    ],
    "Aston Villa": [
        ("Emiliano Martínez", "Goalkeeper"),
        ("Matty Cash", "Defender"),
        ("Ezri Konsa", "Defender"),
        ("Pau Torres", "Defender"),
        ("Lucas Digne", "Defender"),
        ("Douglas Luiz", "Midfielder"),
        ("Boubacar Kamara", "Midfielder"),
        ("John McGinn", "Midfielder"),
        ("Moussa Diaby", "Forward"),
        ("Ollie Watkins", "Forward"),
        ("Leon Bailey", "Forward"),
    ],
    "West Ham United": [
        ("Alphonse Areola", "Goalkeeper"),
        ("Vladimír Coufal", "Defender"),
        ("Kurt Zouma", "Defender"),
        ("Nayef Aguerd", "Defender"),
        ("Emerson Palmieri", "Defender"),
        ("James Ward-Prowse", "Midfielder"),
        ("Edson Álvarez", "Midfielder"),
        ("Lucas Paquetá", "Midfielder"),
        ("Jarrod Bowen", "Forward"),
        ("Michail Antonio", "Forward"),
        ("Mohammed Kudus", "Forward"),
    ],
    "Brighton & Hove Albion": [
        ("Jason Steele", "Goalkeeper"),
        ("Joël Veltman", "Defender"),
        ("Lewis Dunk", "Defender"),
        ("Jan Paul van Hecke", "Defender"),
        ("Pervis Estupiñán", "Defender"),
        ("Pascal Groß", "Midfielder"),
        ("Billy Gilmour", "Midfielder"),
        ("Mahmoud Dahoud", "Midfielder"),
        ("Solly March", "Forward"),
        ("João Pedro", "Forward"),
        ("Kaoru Mitoma", "Forward"),
    ],
}


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # luăm id-urile pozițiilor din tabela positions
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
                (player_name, None, position_id, club_id, 10000000.00),
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Done seeding Premier League players!")


if __name__ == "__main__":
    main()

