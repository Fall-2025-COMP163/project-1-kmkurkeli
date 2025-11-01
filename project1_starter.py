#Kurkeli Kurkeli
#Comp 163 Section 5
#10/20/2025

#AI Use Explanation:
#ChatGPT was used to assist with debugging, and AI was used to explain
#certain strings and blocks of code



# Configuration & Data Tables
# Consistent base and growth values
# Balanced Linear: base + level*growth for each stat
_CLASS_STATS = {
    "Warrior": {
        "base":   {"strength": 8, "magic": 1, "health": 30},  # How much we start with
        "growth": {"strength": 3, "magic": 0, "health": 10},  # How much increases per level
    },
    "Mage": {
        "base":   {"strength": 1, "magic": 9, "health": 20},
        "growth": {"strength": 1, "magic": 4, "health": 6},
    },
    "Rogue": {
        "base":   {"strength": 5, "magic": 5, "health": 16},
        "growth": {"strength": 2, "magic": 2, "health": 4},
    },
    "Cleric": {
        "base":   {"strength": 5, "magic": 8, "health": 28},
        "growth": {"strength": 2, "magic": 3, "health": 8},
    }
}

# AI assisted default starting gold
_DEFAULT_START_GOLD = 50
_SAVE_HEADER = "name,class,level,gold,strength,magic,health"

# Validation helpers

def _normalize_class_name(raw):
    # Normalize input like 'warrior' - 'Warrior' without accepting wrong names.
    # AI assisted Keeps user input flexible but validation strict.
    if not isinstance(raw, str):
        return ""
    return raw.strip().title()


def validate_class(char_class):
    # Return True if char_class is exactly one of the allowed names.
    # AI assisted baseline wording
    return char_class in _CLASS_STATS

def is_valid_class(class_name: str):

    fixed = _normalize_class_name(class_name)
    if validate_class(fixed):
        return "Valid class"
    else:
        return "Invalid class"

# AI Assisted
def compute_stats(class_name: str, level: int):

    fixed = _normalize_class_name(class_name)
    return calculate_stats(fixed, level)   # Calculates using formula from Dict


# Required Functions
# Ai assisted with string explanation
def create_character(name: str, class_name: str, level: int = 1):
    # Validation first
    if not isinstance(name, str) or not name.strip():
        return {}
    cn = _normalize_class_name(class_name)
    if not validate_class(cn):
        return {}
    if not isinstance(level, int) or level < 1:
        return {}

    stats = calculate_stats(cn, level)
    if not stats:   # calculate_stats returns {} on invalid
        return {}

# New Dict containing new data
    return {
        "name": name.strip(),
        "class": cn,
        "level": level,
        "gold": _DEFAULT_START_GOLD,
        "strength": stats["strength"],
        "magic": stats["magic"],
        "health": stats["health"],
    }

 # AI assisted with debugging
 # stat = base + level * growth
def calculate_stats(character_class, level):
    cn = _normalize_class_name(character_class)
    if not validate_class(cn) or not isinstance(level, int) or level < 1:
        return {}  # Empty Dict

    table = _CLASS_STATS[cn]
    base = table["base"]
    growth = table["growth"]
# Stat formula
    strength = base["strength"] + (level - 1) * growth["strength"]
    magic    = base["magic"]    + (level - 1) * growth["magic"]
    health   = base["health"]   + (level - 1) * growth["health"]

    return {"strength": int(strength), "magic": int(magic), "health": int(health)}
# Data Formatter
def _to_csv_line(char: dict):
    return ",".join([
        char.get("name", "").strip(),
        char.get("class", ""),
        str(char.get("level", "")),
        str(char.get("gold", "")),
        str(char.get("strength", "")),
        str(char.get("magic", "")),
        str(char.get("health", "")),
    ])

# Writes character data to a file
def save_character(path, character):
    # Validate required fields
    required = {"name", "class", "level", "gold", "strength", "magic", "health"}
# Makes sure it's a Dict - And required keys are present
    if not isinstance(character, dict) or not required.issubset(character.keys()):
        return "Save failed"
# Getting ready to write in a file
    text = _serialize_exact(character)      # Converts Dict to text format
    f = open(path, "w", encoding="utf-8")   # Opens file for writing
    f.write(text)
    f.close()
    return "Save successful"

def load_character(path):
    # Directly open and read
    f = open(path, "r", encoding="utf-8")
    text = f.read()
    f.close()

    parsed = _deserialize_exact(text)  # Converts back to a Dict
# Checks for error message
    if isinstance(parsed, dict) and "error" in parsed:
        return {}
    return parsed

# Character information showed in correct format
def display_character(character):
    # Display character info. Returns a multi-line string so tests can assert it.
    # AI assisted - matches the same label style users see in save files.
    lines = [
        f"Character Name: {character.get('name','')}",
        f"Class: {character.get('class','')}",
        f"Level: {character.get('level',0)}",
        f"Strength: {character.get('strength',0)}",
        f"Magic: {character.get('magic',0)}",
        f"Health: {character.get('health',0)}",
        f"Gold: {character.get('gold',0)}",
    ]
    
    bs = character.get("backstory", "")
    if bs:
        lines.append(f"Backstory: {bs}")
    return "\n".join(lines)


def level_up(character):
    # Increase character level by 1 and recalculate stats using the same formula.
    # AI assisted with heavy debugging
    if not isinstance(character, dict):
        return "Invalid character data."
# Pulls out class name and checks with list of valid classes
    char_class = character.get("class", "")
    if not validate_class(char_class):
        return "Invalid class on character."

    new_level = int(character.get("level", 1)) + 1   # Take's current level + 1
    character["level"] = new_level   # Updates Dict
# Calculation
    new_stats = calculate_stats(char_class, new_level)
    if "error" in new_stats:
        return new_stats["error"]
# Updates
    character["strength"] = new_stats["strength"]
    character["magic"] = new_stats["magic"]
    character["health"] = new_stats["health"]
    # Keep backstory and gold as is
    return character



# Exact README Format Helpers


# AI assisted debugging
_REQUIRED_ORDER = [
    "Character Name",
    "Class",
    "Level",
    "Strength",
    "Magic",
    "Health",
    "Gold",
]

def _serialize_exact(character):
    # Create a text block in the exact label order that is required
    name = character.get("name", "")
    cls  = character.get("class", "")
    lvl  = int(character.get("level", 1))
    strn = int(character.get("strength", 0))
    mag  = int(character.get("magic", 0))
    hp   = int(character.get("health", 0))
    gold = int(character.get("gold", 0))

    lines = [
        f"Character Name: {name}",
        f"Class: {cls}",
        f"Level: {lvl}",
        f"Strength: {strn}",
        f"Magic: {mag}",
        f"Health: {hp}",
        f"Gold: {gold}",
    ]
    return "\n".join(lines) + "\n"


def _is_int_string(s):
    # AI assisted - Simple check to be able to convert to int more simple
    if not isinstance(s, str):
        return False
    t = s.strip()
    if t.startswith("-"):   # Handles Negative numbers
        t = t[1:]
    return t.isdigit()


def _deserialize_exact(text):
    # Parse the exact format back into a character dict - AI assisted
    if not isinstance(text, str) or not text.strip():     # After removing spaces string can't be empty
        return {"error": "Empty file"}
    # Splits the text into separate lines
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]    # One per field
    if len(lines) < 7:
        return {"error": "Missing lines"}

    # Parse into a simple map
    data = {}
    for ln in lines:
        if ": " not in ln:
            # tolerate extra lines like "Backstory:
            continue
        # split once
        p = ln.split(": ", 1)
        if len(p) != 2:
            continue
        label, value = p[0].strip(), p[1].strip()
        data[label] = value

    # Ensure required labels exist
    for lbl in _REQUIRED_ORDER:
        if lbl not in data:
            return {"error": f"Missing field: {lbl}"}

    name = data.get("Character Name", "")     # Pulls out name
    cls  = _normalize_class_name(data.get("Class", ""))       # Normalizes the class name

    # Validate integers
    lvls = data.get("Level", "1")
    strs = data.get("Strength", "0")
    mags = data.get("Magic", "0")
    hps  = data.get("Health", "0")
    glds = data.get("Gold", "0")
    # Makes sure it's a valid integer string
    if not (_is_int_string(lvls) and _is_int_string(strs) and _is_int_string(mags) and _is_int_string(hps) and _is_int_string(glds)):
        return {"error": "Non-integer numeric field"}

    lvl  = int(lvls)
    strn = int(strs)
    mag  = int(mags)
    hp   = int(hps)
    gold = int(glds)

    if not validate_class(cls):
        return {"error": "Invalid class in file"}
    # Clean Dictionary after all invalidating
    # AI assisted - We keep parsed numbers; you could force formula values by recalculating.
    return {
        "name": name,
        "class": cls,
        "level": lvl,
        "strength": strn,
        "magic": mag,
        "health": hp,
        "gold": gold,
        # Backstory is optional; not part of the required file format.
        "backstory": generate_backstory(name, cls),
    }

# Backstory Generator


def generate_backstory(name, char_class):
    # A short single-sentence backstory
    # AI assisted Wording draft
    templates = {
        "Warrior": f"{name} trained on the frontier, earning scars long before glory called.",
        "Mage":    f"{name} mastered forbidden sigils, trading comfort for arcane insight.",
        "Rogue":   f"{name} learned to survive in the alleys, quick with wit and quicker with hands.",
        "Cleric":  f"{name} swore a quiet oath, bringing light where hope had thinned.",
    }
    return templates.get(char_class, f"{name} wanders with untold stories.")

if __name__ == "__main__":

    hero = create_character(name="Aria", class_name="Warrior", level=1)
    print(hero)
# Saves character data to a file
    saved = save_character("aria.txt", hero)
    print("Save result:", saved)
# Loads back in
    loaded = load_character("aria.txt")
    print(loaded
