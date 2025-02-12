from fuzzywuzzy import process
import re
def match_attr(lines):
    item_name = lines[0]
    rarity = None
    primary = {}
    secondary = {}

    for line in lines[1:]:
        rarity_match = re.search(r'Rarity\s*:\s*(\w+)', line)
        primary_match = re.search(r'([\w\s]+)(\d+)', line)
        if primary_match:
            result = smart_match(primary_match.group(1))
            if result:
                print(f"Match: {result[0]} with confidence {result[1]}%")
                primary[result[0]] = int(primary_match.group(2))

        secondary_match = re.search(r'(^[\+l\.\d]+)%*\s*([\w\s]+)', line)
        if secondary_match:
            result = smart_match(secondary_match.group(2))
            if result:
                print(f"Match: {result[0]} with confidence {result[1]}%")
                num_fixed=secondary_match.group(1).replace('l', '1')
                if '.' in num_fixed:
                    secondary[result[0]] = float(num_fixed)
                else:
                    secondary[result[0]] = int(num_fixed)

        if rarity_match:
            rarity = rarity_match.group(1)
    return {"item_name":item_name,"rarity":rarity,"primary":primary,"secondary":secondary}

def smart_match(input_word, threshold=70):
    field_list = [
    "action_speed", "agility", "armor_penetration", "armor_rating", 
    "additional_armor_rating", "buff_duration_bonus", "cooldown_reduction_bonus", 
    "debuff_duration_bonus", "dexterity", "headshot_damage_reduction", 
    "equip_speed", "knowledge", "luck", "magic_penetration", 
    "magic_resistance", "magical_damage", "additional_magical_damage", 
    "magical_damage_bonus", "magical_damage_reduction", "true_magical_damage", 
    "magical_healing", "magical_interaction_speed", "magical_power", 
    "magic_weapon_damage", "manual_dexterity", "max_health", 
    "max_health_bonus", "additional_memory_capacity", "memory_capacity_bonus", 
    "move_speed", "additional_move_speed", "move_speed_bonus", 
    "persuasiveness", "additional_physical_damage", "physical_damage_bonus", 
    "physical_damage_reduction", "true_physical_damage", "physical_healing", 
    "physical_power", "weapon_damage", "additional_weapon_damage", 
    "all_attributes", "projectile_damage_reduction", "regular_interaction_speed", 
    "resourcefulness", "spell_casting_speed", "strength", 
    "undead_damage_bonus", "additional_utility_effectiveness", 
    "utility_effectiveness_bonus", "vigor", "additional_weight_limit", 
    "weight_limit_bonus", "will"
]
    """
    Matches input word to the closest field name using fuzzy matching.
    
    Args:
    - input_word: The word to match.
    - field_list: List of target fields.
    - threshold: Minimum confidence for a valid match (0-100).
    
    Returns:
    - Best match and confidence score or None if below threshold.
    """
    match, confidence = process.extractOne(input_word, field_list)
    return (match, confidence) if confidence >= threshold else None

# Example Usage
input_term = "magicl_damge"  # Intentional typo
result = smart_match(input_term)

if result:
    print(f"Match: {result[0]} with confidence {result[1]}%")
else:
    print("No confident match found.")
# Function to convert field names to acronyms

def attribute_to_acrynom(field):
    words = re.split(r'_', field)  # Split by underscores
    acronym = ''.join(word[0].upper() for word in words)
    return acronym