# Importieren der benötigten Module
import csv
import random
import time
import webbrowser
from collections import defaultdict

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

# Funktion zur Simulation eines Spiels mit zufälliger Punktevergabe
def simulate_match():
    team1_score = 0
    team2_score = 0

    for _ in range(3):
        winner = random.choice([1, 2])  # Zufälliger Gewinner für dieses Spiel
        if winner == 1:
            team1_score += 1
        else:
            team2_score += 1

        print(f"Spielstand: {team1_score} - {team2_score}")
        time.sleep(2)  # 2 Sekunden Pause

    return team1_score, team2_score

# Funktion zum Speichern des Spielergebnisses in einer CSV-Datei
def save_result(team1, team2, team1_score, team2_score):
    result = []
    if team1_score > team2_score:
        winner, loser = team1, team2
    else:
        winner, loser = team2, team1

    result.append(','.join([player.name for player in winner]))
    result.append(','.join([player.name for player in loser]))

    with open('ergebnisse.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(result)

# Hauptfunktion zur Ausführung des Programms
def main():
    players = read_players('Fifa_Players_2018_reduziert.csv')
    team1, team2 = distribute_players(players)
    print("Willkommen zum Fußballspiel-Simulator!")
    time.sleep(2)

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

    print("\nTeam 1:")
    for player in team1:
        print(f"  {player.name} ({', '.join(player.positions)})")
    time.sleep(2)

    print("\nTeam 2:")
    for player in team2:
        print(f"  {player.name} ({', '.join(player.positions)})")
    time.sleep(2)

    print("\nSpielstand: 0 - 0")
    team1_score, team2_score = simulate_match()
    print(f"\nEndstand: Team 1, {team1_score} - {team2_score}, Team 2")
    save_result(team1, team2, team1_score, team2_score)

    # Wetten-Ergebnis
    if chosen_team:
        if (team1_score > team2_score and chosen_team == team1) or (team1_score < team2_score and chosen_team == team2):
            print("Glückwunsch, Sie haben gewonnen!")
            webbrowser.open("https://imgs.search.brave.com/oLBoz-5D1T17J2gQxKegf4LWOStHkupvD5nYOLtlDdY/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9pLnBp/bmltZy5jb20vb3Jp/Z2luYWxzL2RmL2E0/LzVkL2RmYTQ1ZDc1/NjRlZGFkMmQyMWY2/ZWU3OWJhZWM5Y2I5/LmpwZw")
        else:
            print("Tut mir leid, Sie haben verloren.")
            webbrowser.open("https://youtu.be/xvFZjo5PgG0")

if __name__ == "__main__":
    main()

