import csv
import random
import time
import webbrowser
import sqlite3

# Definieren der Spielerklasse
class Spieler:
    def __init__(self, name, full_name, birth_date, age, height_cm, weight_kgs, positions, nationality, overall_rating, potential, value_euro, wage_euro):
        self.name = name
        self.full_name = full_name
        self.birth_date = birth_date
        self.age = age
        self.height_cm = height_cm
        self.weight_kgs = weight_kgs
        self.positions = positions.split(',')
        self.nationality = nationality
        self.overall_rating = int(overall_rating) if overall_rating.isdigit() else 0
        self.potential = potential
        self.value_euro = value_euro
        self.wage_euro = wage_euro

# Funktion zum Einlesen der Spielerdaten aus einer CSV-Datei
def read_players(filename):
    players = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            player = Spieler(row['name'], row['full_name'], row['birth_date'], row['age'], row['height_cm'], row['weight_kgs'], row['positions'], row['nationality'], row['overall_rating'], row['potential'], row['value_euro'], row['wage_euro'])
            players.append(player)
    return players

# Funktion zur Verteilung der Spieler auf zwei Teams
def distribute_players(players, team_size=10):
    random.shuffle(players)
    teams = [players[:team_size], players[team_size:team_size*2]]
    return teams

# Funktion zur Berechnung der Durchschnittsbewertung eines Teams
def calculate_team_rating(team):
    total_rating = sum(player.overall_rating for player in team)
    return total_rating / len(team)

# Funktion zur Simulation eines Spiels basierend auf den Teamwertungen
def simulate_match(team1, team2):
    team1_score = 0
    team2_score = 0

    team1_rating = calculate_team_rating(team1)
    team2_rating = calculate_team_rating(team2)

    for _ in range(9):
        # Adjust the probabilities based on team ratings
        if random.uniform(0, team1_rating + team2_rating) < team1_rating:
            team1_score += 1
        else:
            team2_score += 1

        print(f"Spielstand: {team1_score} - {team2_score}")
        time.sleep(0.5)

    return team1_score, team2_score

# Funktion zum Speichern des Spielergebnisses in einer SQLite-Datenbank
def save_result_to_db(team1, team2, team1_score, team2_score):
    conn = sqlite3.connect('ergebnisse.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS results
                      (id INTEGER PRIMARY KEY, winner TEXT, loser TEXT, team1_score INTEGER, team2_score INTEGER)''')

    if team1_score > team2_score:
        winner, loser = team1, team2
    else:
        winner, loser = team2, team1

    winner_names = ','.join([player.name for player in winner])
    loser_names = ','.join([player.name for player in loser])

    cursor.execute('INSERT INTO results (winner, loser, team1_score, team2_score) VALUES (?, ?, ?, ?)',
                   (winner_names, loser_names, team1_score, team2_score))

    conn.commit()
    conn.close()

# Hauptfunktion zur Ausführung des Programms
def main():
    players = read_players('Fifa_Players_2018_reduziert.csv')
    team1, team2 = distribute_players(players)
    print("Willkommen zum Fußballspiel-Simulator!")
    time.sleep(0.5)

    print("\nTeam 1:")
    for player in team1:
        print(f"  {player.name} ({', '.join(player.positions)})")
    time.sleep(0.5)

    print("\nTeam 2:")
    for player in team2:
        print(f"  {player.name} ({', '.join(player.positions)})")
    time.sleep(0.5)

    # Wetten-Option
    bet = input("Möchten Sie auf ein Team wetten? (j/n) ")
    if bet.lower() == "j":
        team_choice = input("Auf welches Team möchten Sie wetten? (1/2) ")
        if team_choice == "1":
            chosen_team = team1
        elif team_choice == "2":
            chosen_team = team2
        else:
            print("Ungültige Eingabe. Kein Wetten.")
            chosen_team = None
    else:
        chosen_team = None

    print("\nSpielstand: 0 - 0")
    team1_score, team2_score = simulate_match(team1, team2)
    print(f"\nEndstand: Team 1, {team1_score} - {team2_score}, Team 2")
    save_result_to_db(team1, team2, team1_score, team2_score)

    # Wetten-Ergebnis
    if chosen_team:
        if (team1_score > team2_score and chosen_team == team1) or (team1_score < team2_score and chosen_team == team2):
            print("Glückwunsch, Sie haben gewonnen!")
            webbrowser.open("https://t3.ftcdn.net/jpg/02/82/23/94/360_F_282239447_9JUkxLmUPzBvOrEAXVEx2GpNd1EkPOSO.jpg")
        else:
            print("Sie haben verloren.")
            webbrowser.open("https://i1.sndcdn.com/artworks-BBMnwmO6ymZ90v3V-zYlw4g-t500x500.jpg")

if __name__ == "__main__":
    main()
