import json
from utils.scraper import scrape_character_data

# List of set codes and unit numbers
# set_codes = ["av60", "smba", "btu", "av4e", "hgpc", "xmxssop", "xmxs", "msdp", "ff:wotr", "wotr", "ff2021", "affe", "em", "xmrf", "ff:xmrf", "ww80"]  # Add all set codes
set_codes = ["av60"]
unit_numbers = list(range(1,103))

# Scrape the character endpoints
character_data = scrape_character_data(set_codes, unit_numbers)

# Write the data to a JSON file
# with open('character_data.json', 'w') as f:
with open(f'character_data_{set_codes[0]}.json', 'w') as f:
    json.dump(character_data, f)
