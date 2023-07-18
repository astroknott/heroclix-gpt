from bs4 import BeautifulSoup
from utils.character_parser import parse_character_data
from utils.make_request import make_request

def scrape_character_data(set_codes, unit_numbers):
    base_url = "https://www.hcrealms.com/forum/units/units_bbcode.php?id="
    all_character_data = []

    for set_code in set_codes:
        skip_if_less = 0
        for unit_number in unit_numbers:
            if unit_number < skip_if_less:
                continue
            units = []
            
            def get_character_table_from_suffix(suffix):
                path = str(unit_number).zfill(3) + suffix
                url = base_url + set_code + path
                html = make_request(url)
                soup = BeautifulSoup(html, 'html.parser')
                character_table = soup.find_all('textarea')[1].string
                print(character_table)

                return character_table

            # try base path
            base_table = get_character_table_from_suffix('')
            if base_table:
                units.append(base_table)
                v_table = get_character_table_from_suffix('v')
                if v_table:
                    units.append(v_table)
                    e_table = get_character_table_from_suffix('e')
                    if e_table:
                        units.append(e_table)
            else:
                a_table = get_character_table_from_suffix('a')
                if a_table:
                    b_table = get_character_table_from_suffix('b')
                    units.extend([a_table, b_table])
                else:
                    skip_if_less = 99
                             
            if len(units) > 0:
                for unit in units:
                    character_data = parse_character_data(unit)
                    all_character_data.append(character_data)
    return all_character_data
