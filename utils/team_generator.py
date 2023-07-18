import random 
from utils.synergy_bonus import synergy_bonus


def generate_team(character_data, standard_powers_data, base_character_position = 0):
    """
    Generate a team of characters under 300 points with the highest possible effectiveness.
    """
    # Initialize the team and total points
    base_character = character_data[base_character_position]
    team = [base_character]
    total_points = base_character['points']
    random.shuffle(character_data)
    
    def rescale_value(old_value, old_min, old_max, new_min, new_max):
        return (((old_value - old_min) / (old_max - old_min)) * (new_max - new_min)) + new_min
    # Define powers that allow multiple actions or free actions
    multiple_actions_powers = ['RUNNING SHOT', 'CHARGE', 'HYPERSONIC SPEED', 'FLURRY']
    free_actions_powers = ['OUTWIT', 'PERPLEX', 'PROBABILITY CONTROL', 'TELEKINESIS', 'LEADERSHIP']
    slot_type_list = ['speed', 'attack', 'defense', 'damage']
    display_config = {}
    display_config.update({
        base_character['name']: 'base'
    })
    # Loop through the shuffled list of characters
    for character in character_data:
        set_number = int(character['id'][4:7])
        
        # skip if base character
        if character['name'] == base_character['name']:
            continue
        # skip if won't fit on team
        if total_points + character['points'] > 300:
            continue
        # skip if a same name character is already on team
        for teammate in team:
            if teammate['name'] in character['name']:
                continue
            
        # Calculate character lifespan (number of non-KO clicks)
        lifespan = 0
        for click in character['dial_data']:
            if click['speed']['power'] == 'ko':
                break
            lifespan += 1

        # Calculate action economy by counting the number of clicks with multiple action powers or free action powers
        action_economy = 0
        action_powers = []
        for click in character['dial_data']:
            for idx, slot in enumerate(click.values()):
                slot_type = slot_type_list[idx]
                power_color = slot['power']
                if power_color == 'none' or power_color == 'special' or power_color == 'ko':
                    continue
                power = standard_powers_data[slot_type][power_color]
                for key,val in power.items():
                    action_powers.append(key)
        for power_name in set(action_powers):
            if power_name in multiple_actions_powers or power_name in free_actions_powers:
                action_economy += 1

        # Loop through the existing team members and add the synergy bonus to the effectiveness score
        synergy_score = 0
        for team_member in team:
            synergy_score += synergy_bonus(character, team_member)

        lifespan_weighted = lifespan * 0.01
        action_economy_weighted = action_economy * 1.8
        synergy_score_weighted = synergy_score * 2
        effectiveness = lifespan_weighted + action_economy_weighted + synergy_score_weighted

        effectiveness_to_points = effectiveness / character['points']
        rarity = rescale_value(set_number, 1, 110, 1, .8)
        effectiveness_for_rarity = effectiveness_to_points * rarity

        if effectiveness_for_rarity >= .45:
            team.append(character)
            display_config.update({
                character['name']: {
                    'effectiveness': effectiveness_for_rarity
                }})
            total_points += character['points']

        # If the team is full (reached the points limit), stop adding characters
        if total_points >= 295:
            break

    # After creating the initial team, iterate through the character data again to see if any character should be replaced
    # for character in character_data:
    #     if character not in team:
    #         for i, team_member in enumerate(team):
    #             # If a character has a higher effectiveness score and can fit in the team when replacing a current team member, do so
    #             if character['effectiveness_score'] > team_member['effectiveness_score'] and \
        #                total_points - team_member['points'] + character['points'] <= 300:
    #                 total_points = total_points - team_member['points'] + character['points']
    #                 team[i] = character
    
    # Return the final team
    return { 'team': team, 'display': display_config}
