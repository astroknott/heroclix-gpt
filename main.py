import json
from utils.team_generator import generate_team

# Load the data
with open("data/character_data_av60.json", "r") as file:
    character_data = json.load(file)
with open("data/powers.json", "r") as file:
    standard_powers_data = json.load(file)
with open("data/improved_abilities.json", "r") as file:
    improved_abilities_data = json.load(file)
with open("data/keyphrase_abilities.json", "r") as file:
    keyphrase_abilities_data = json.load(file)
with open("data/team_abilities.json", "r") as file:
    team_abilities_data = json.load(file)

# Generate the team
team_result = generate_team(character_data, standard_powers_data)

# Print the team
for idx, character in enumerate(team_result['team']):
    if not idx:
        continue
    info = team_result['display'][character['name']]

    print({character['name']: {
        'Effectiveness': info['effectiveness'],
    }})
