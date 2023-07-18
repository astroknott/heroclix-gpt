# Updating the team building strategy to include team abilities and re-running the team generation process

def synergy_bonus(character1, character2):
    """
    Calculates a synergy bonus between two characters.
    """
    bonus = 0

    # Check for shared keywords
    shared_keywords = list(set(character1['keywords']) & set(character2['keywords']))
    for keyword in shared_keywords:
        bonus += 2  # Increment synergy bonus if shared keyword has benefits
            # Check for synergy in special powers
        for power_name, power_text in character1['special_abilities'].items():
            if "keyword" in power_text and "friendly character" in power_text:
                bonus += 2
        for power_name, power_text in character2['special_abilities'].items():
            if "keyword" in power_text and "friendly character" in power_text:
                bonus += 2  # Increment synergy bonus if shared special power has benefits

    # Check for shared team abilities
    if character1['team'] == character2['team']:
        bonus += 1  # Increment synergy bonus if shared team ability has benefits
        for power_name, power_text in character1['special_abilities'].items():
            if "friendly character" in power_text and "team ability" in power_text:
                bonus += 2

    return bonus
