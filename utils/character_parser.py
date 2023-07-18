import re

def parse_character_data(html):
    character_data = {}
    
    # Parse the character ID and name
    search_result = re.search(r"(\w+)\s+\[b\](.+)\[/b\]", html)

    if search_result is not None:
        character_data["id"], character_data["name"] = search_result.groups()
    else:
        print(f"Warning: Could not find ID and name in the following html content:\n{html}")

    # Parse the team and keywords as lists
    for field in ["Team", "Keywords"]:
        match = re.search(fr"{field}:\s+\[b\](.+)\[/b\]", html)
        if match:
            split_char = "|" if field == "Team" else ", "
            character_data[field.lower()] = match.group(1).split(split_char)

    # Parse the points as integer
    match = re.search(r"Points:\s+\[b\](\d+)\[/b\]", html)
    if match:
        character_data["points"] = int(match.group(1))

    # Parse the range and bolts as integers
    range_match = re.search(r"Range:\s+\[b\](.+)\[/b\]", html)
    if range_match:
        range_info = range_match.group(1)
        character_data["range"] = int(re.search(r"(\d+)", range_info).group(1))
        character_data["bolts"] = range_info.count(':bolt:')

    # Parse the dial header data
    dial_header_data = re.findall(r"\[icon\](.+?)\[/icon\]", html)
    character_data["dial_header_data"] = dial_header_data

    # Parse the dial data, converting integers where possible
    dial_data = re.findall(r"\[click\](.+?)\[/click\]", html)
    character_data["dial_data"] = []
    for click in dial_data:
        slots = re.findall(r"\[slot=(.+?)\](.+?)\[/slot\]", click)
        click_data = {}
        keys_list = ['speed', 'attack', 'defense', 'damage']
        for i, (key, value) in enumerate(slots):  # iterate over the available slots
            click_data[keys_list[i]] = {'power': key, 'value': int(value) if value.isdigit() else value}
        character_data["dial_data"].append(click_data)

    # Parse the special abilities
    special_abilities = re.findall(r"\[b\]\(([^)]+)\) (.+?)?: \[/b\](.+?)(?=\[b\]|\Z)", html, re.DOTALL)
    character_data["special_abilities"] = {}
    for ability, ability_name, description in special_abilities:
        ability_key = f"{ability} Targeting" if ability == "Improved" else f"{ability_name} ({ability})"
        description = re.sub("<.*?>", "", description)  # remove HTML tags
        character_data["special_abilities"][ability_key.strip()] = description.strip()

    return character_data
