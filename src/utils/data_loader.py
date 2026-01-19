# ----------------------------------
# IMPORTS
# ----------------------------------
import json
from config.settings import DATA_DIR

# ----------------------------------
# FUNCTIONS
# ----------------------------------
def load_achievements():
    filepath = DATA_DIR / "achievements.json"

    if not filepath.exists():
        return {}

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_category1_keys():
    achievements = load_achievements()
    return list(achievements.keys())
