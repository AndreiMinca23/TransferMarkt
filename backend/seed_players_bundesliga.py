import os
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://transfer_user:transfer_pass@db:5432/transfermarkt",
)

# club -> listă de (nume jucător, poziție)
SQUADS = {
    "Bayern Munich": [
        ("Manuel Neuer", "Goalkeeper"),
        ("Joshua Kimmich", "Defender"),
        ("Dayot Upamecano", "Defender"),
        ("Matthijs de Ligt", "Defender"),
        ("Alphonso Davies", "Defender"),
        ("Leon Goretzka", "Midfielder"),
        ("Jamal Musiala", "Midfielder"),
        ("Thomas Müller", "Midfielder"),
        ("Kingsley Coman", "Forward"),
        ("Serge Gnabry", "Forward"),
        ("Harry Kane", "Forward"),
    ],
    "Borussia Dortmund": [
        ("Gregor Kobel", "Goalkeeper"),
        ("Thomas Meunier", "Defender"),
        ("Mats Hummels", "Defender"),
        ("Nico Schlotterbeck", "Defender"),
        ("Raphaël Guerreiro", "Defender"),
        ("Emre Can", "Midfielder"),
        ("Jude Bellingham", "Midfielder"),
        ("Julian Brandt", "Midfielder"),
        ("Karim Adeyemi", "Forward"),
        ("Donyell Malen", "Forward"),
        ("Youssoufa Moukoko", "Forward"),
    ],
    "RB Leipzig": [
        ("Peter Gulácsi", "Goalkeeper"),
        ("Benjamin Henrichs", "Defender"),
        ("Willi Orbán", "Defender"),
        ("Josko Gvardiol", "Defender"),
        ("David Raum", "Defender"),
        ("Konrad Laimer", "Midfielder"),
        ("Xaver Schlager", "Midfielder"),
        ("Dominik Szoboszlai", "Midfielder"),
        ("Christopher Nkunku", "Forward"),
        ("Timo Werner", "Forward"),
        ("Dani Olmo", "Forward"),
    ],
    "Bayer Leverkusen": [
        ("Lukáš Hrádecký", "Goalkeeper"),
        ("Jeremie Frimpong", "Defender"),
        ("Jonathan Tah", "Defender"),
        ("Edmond Tapsoba", "Defender"),
        ("Piero Hincapié", "Defender"),
        ("Robert Andrich", "Midfielder"),
        ("Exequiel Palacios", "Midfielder"),
        ("Florian Wirtz", "Midfielder"),
        ("Moussa Diaby", "Forward"),
        ("Patrik Schick", "Forward"),
        ("Adam Hložek", "Forward"),
    ],
    "Borussia Mönchengladbach": [
        ("Yann Sommer", "Goalkeeper"),
        ("Stefan Lainer", "Defender"),
        ("Matthias Ginter", "Defender"),
        ("Nico Elvedi", "Defender"),
        ("Ramy Bensebaini", "Defender"),
        ("Florian Neuhaus", "Midfielder"),
        ("Christoph Kramer", "Midfielder"),
        ("Lars Stindl", "Midfielder"),
        ("Jonas Hofmann", "Forward"),
        ("Alassane Pléa", "Forward"),
        ("Marcus Thuram", "Forward"),
    ],
    "Eintracht Frankfurt": [
        ("Kevin Trapp", "Goalkeeper"),
        ("Tuta", "Defender"),
        ("Evan Ndicka", "Defender"),
        ("Kristijan Jakic", "Defender"),
        ("Christopher Lenz", "Defender"),
        ("Djibril Sow", "Midfielder"),
        ("Sebastian Rode", "Midfielder"),
        ("Mario Götze", "Midfielder"),
        ("Jesper Lindstrøm", "Forward"),
        ("Randal Kolo Muani", "Forward"),
        ("Daichi Kamada", "Forward"),
    ],
    "Wolfsburg": [
        ("Koen Casteels", "Goalkeeper"),
        ("Ridle Baku", "Defender"),
        ("Maxence Lacroix", "Defender"),
        ("Sebastiaan Bornauw", "Defender"),
        ("Jérôme Roussillon", "Defender"),
        ("Maximilian Arnold", "Midfielder"),
        ("Yannick Gerhardt", "Midfielder"),
        ("Felix Nmecha", "Midfielder"),
        ("Patrick Wimmer", "Forward"),
        ("Lukas Nmecha", "Forward"),
        ("Jonas Wind", "Forward"),
    ],
    "SC Freiburg": [
        ("Mark Flekken", "Goalkeeper"),
        ("Lukas Kübler", "Defender"),
        ("Matthias Ginter", "Defender"),
        ("Philipp Lienhart", "Defender"),
        ("Christian Günter", "Defender"),
        ("Nicolas Höfler", "Midfielder"),
        ("Maximilian Eggestein", "Midfielder"),
        ("Vincenzo Grifo", "Midfielder"),
        ("Roland Sallai", "Forward"),
        ("Michael Gregoritsch", "Forward"),
        ("Lucas Höler", "Forward"),
    ],
    "Union Berlin": [
        ("Frederik Rønnow", "Goalkeeper"),
        ("Christopher Trimmel", "Defender"),
        ("Robin Knoche", "Defender"),
        ("Danilho Doekhi", "Defender"),
        ("Niko Gießelmann", "Defender"),
        ("Rani Khedira", "Midfielder"),
        ("Janik Haberer", "Midfielder"),
        ("Aïssa Laïdouni", "Midfielder"),
        ("Sheraldo Becker", "Forward"),
        ("Jordan Pefok", "Forward"),
        ("Kevin Behrens", "Forward"),
    ],
    "VfB Stuttgart": [
        ("Florian Müller", "Goalkeeper"),
        ("Konstantinos Mavropanos", "Defender"),
        ("Waldemar Anton", "Defender"),
        ("Hiroki Ito", "Defender"),
        ("Borna Sosa", "Defender"),
        ("Wataru Endo", "Midfielder"),
        ("Atakan Karazor", "Midfielder"),
        ("Chris Führich", "Midfielder"),
        ("Tiago Tomás", "Forward"),
        ("Serhou Guirassy", "Forward"),
        ("Silas Katompa Mvumpa", "Forward"),
    ],
}


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # mapăm numele pozițiilor -> id
    cur.execute("SELECT id, name FROM positions;")
    pos_rows = cur.fetchall()
    pos_by_name = {name: pid for pid, name in pos_rows}

    for club_name, players in SQUADS.items():
        # găsim clubul după nume
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
                (player_name, None, position_id, club_id, 8000000.00),
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Done seeding Bundesliga players!")


if __name__ == "__main__":
    main()
