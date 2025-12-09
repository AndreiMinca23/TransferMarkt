import os
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://transfer_user:transfer_pass@db:5432/transfermarkt",
)

SQUADS = {
    "Ajax": [
        ("Gerónimo Rulli", "Goalkeeper"),
        ("Devyne Rensch", "Defender"),
        ("Jurriën Timber", "Defender"),
        ("Calvin Bassey", "Defender"),
        ("Owen Wijndal", "Defender"),
        ("Edson Álvarez", "Midfielder"),
        ("Kenneth Taylor", "Midfielder"),
        ("Steven Berghuis", "Midfielder"),
        ("Dusan Tadic", "Forward"),
        ("Brian Brobbey", "Forward"),
        ("Steven Bergwijn", "Forward"),
    ],
    "PSV Eindhoven": [
        ("Walter Benítez", "Goalkeeper"),
        ("Jordan Teze", "Defender"),
        ("André Ramalho", "Defender"),
        ("Olivier Boscagli", "Defender"),
        ("Patrick van Aanholt", "Defender"),
        ("Ibrahim Sangaré", "Midfielder"),
        ("Joey Veerman", "Midfielder"),
        ("Guus Til", "Midfielder"),
        ("Johan Bakayoko", "Forward"),
        ("Luuk de Jong", "Forward"),
        ("Noa Lang", "Forward"),
    ],
    "Feyenoord": [
        ("Justin Bijlow", "Goalkeeper"),
        ("Lutsharel Geertruida", "Defender"),
        ("Gernot Trauner", "Defender"),
        ("David Hancko", "Defender"),
        ("Quilindschy Hartman", "Defender"),
        ("Mats Wieffer", "Midfielder"),
        ("Quinten Timber", "Midfielder"),
        ("Calvin Stengs", "Midfielder"),
        ("Igor Paixão", "Forward"),
        ("Santiago Giménez", "Forward"),
        ("Alireza Jahanbakhsh", "Forward"),
    ],
    "AZ Alkmaar": [
        ("Mathew Ryan", "Goalkeeper"),
        ("Yukinari Sugawara", "Defender"),
        ("Sam Beukema", "Defender"),
        ("Pantelis Hatzidiakos", "Defender"),
        ("David Møller Wolfe", "Defender"),
        ("Jordy Clasie", "Midfielder"),
        ("Tijjani Reijnders", "Midfielder"),
        ("Dani de Wit", "Midfielder"),
        ("Jens Odgaard", "Forward"),
        ("Vangelis Pavlidis", "Forward"),
        ("Myron van Brederode", "Forward"),
    ],
    "FC Utrecht": [
        ("Vasilis Barkas", "Goalkeeper"),
        ("Sean Klaiber", "Defender"),
        ("Mike van der Hoorn", "Defender"),
        ("Modibo Sagnan", "Defender"),
        ("Nikos Ioannidis", "Defender"),  # poziție generică
        ("Jens Toornstra", "Midfielder"),
        ("Can Bozdogan", "Midfielder"),
        ("Taylor Booth", "Midfielder"),
        ("Othmane Boussaid", "Forward"),
        ("Bas Dost", "Forward"),
        ("Anastasios Douvikas", "Forward"),
    ],
    "Vitesse": [
        ("Bartosz Białkowski", "Goalkeeper"),  # jucător generic GK
        ("Carlens Arcus", "Defender"),
        ("Enzo Cornelisse", "Defender"),
        ("Dominik Oroz", "Defender"),
        ("Maximilian Wittek", "Defender"),
        ("Matúš Bero", "Midfielder"),
        ("Marco van Ginkel", "Midfielder"),
        ("Million Manhoef", "Midfielder"),
        ("Nicolò Fagioli", "Midfielder"),  # generic
        ("Mohamed Sankoh", "Forward"),
        ("Loïs Openda", "Forward"),
    ],
    "Heerenveen": [
        ("Xavier Mous", "Goalkeeper"),
        ("Milan van Ewijk", "Defender"),
        ("Syb van Ottele", "Defender"),
        ("Pawel Bochniewicz", "Defender"),
        ("Rami Kaib", "Defender"),
        ("Thom Haye", "Midfielder"),
        ("Simon Olsson", "Midfielder"),
        ("Anas Tahiri", "Midfielder"),
        ("Amin Sarr", "Forward"),
        ("Sydney van Hooijdonk", "Forward"),
        ("Osame Sahraoui", "Forward"),
    ],
    "FC Twente": [
        ("Lars Unnerstall", "Goalkeeper"),
        ("Giovanni Troupée", "Defender"),
        ("Mees Hilgers", "Defender"),
        ("Robin Pröpper", "Defender"),
        ("Gijs Smal", "Defender"),
        ("Ramiz Zerrouki", "Midfielder"),
        ("Michal Sadílek", "Midfielder"),
        ("Vaclav Cerny", "Midfielder"),
        ("Daan Rots", "Forward"),
        ("Ricky van Wolfswinkel", "Forward"),
        ("Manfred Ugalde", "Forward"),
    ],
    "Groningen": [
        ("Michael Verrips", "Goalkeeper"),
        ("Damil Dankerlui", "Defender"),
        ("Radinio Balker", "Defender"),
        ("Mike te Wierik", "Defender"),
        ("Gabriel Gudmundsson", "Defender"),
        ("Laros Duarte", "Midfielder"),
        ("Tomas Suslov", "Midfielder"),
        ("Thom van Bergen", "Midfielder"),
        ("Jørgen Strand Larsen", "Forward"),
        ("Pelé van Anholt", "Forward"),  # generic
        ("Florian Krüger", "Forward"),
    ],
    "Sparta Rotterdam": [
        ("Nick Olij", "Goalkeeper"),
        ("Shurandy Sambo", "Defender"),
        ("Bart Vriends", "Defender"),
        ("Adil Auassar", "Defender"),
        ("Mica Pinto", "Defender"),
        ("Dirk Abels", "Midfielder"),
        ("Sven Mijnans", "Midfielder"),
        ("Joshua Kitolano", "Midfielder"),
        ("Koki Saito", "Forward"),
        ("Tobias Lauritsen", "Forward"),
        ("Vito van Crooij", "Forward"),
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
                (player_name, None, position_id, club_id, 4000000.00),
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Done seeding Eredivisie players!")


if __name__ == "__main__":
    main()

