# ----------------------------------
# IMPORTS
# ----------------------------------
import json
import pandas as pd
from config.settings import DATA_DIR

# ----------------------------------
# FUNCTIONS
# ----------------------------------
def ingest_achievements():
    excel_path = DATA_DIR / "achievements.xlsx"
    json_path = DATA_DIR / "achievements.json"

    df = pd.read_excel(excel_path)

    result = {}

    for _, row in df.iterrows():
        category1 = str(row["Category 1"]) if pd.notna(row["Category 1"]) else "Uncategorized"
        category2 = str(row["Category 2"]) if pd.notna(row["Category 2"]) else None

        if category1 not in result:
            result[category1] = {}

        achievement_data = {
            "name": str(row["Name"]) if pd.notna(row["Name"]) else None,
            "icon": str(row["Icon"]) if pd.notna(row["Icon"]) else None,
            "mode": str(row["Mode"]) if pd.notna(row["Mode"]) else None,
            "window": str(row["Window"]) if pd.notna(row["Window"]) else None,
            "base": str(row["Base"]) if pd.notna(row["Base"]) else None,
            "normal": str(row["Normal"]) if pd.notna(row["Normal"]) else None,
            "elite": str(row["Elite"]) if pd.notna(row["Elite"]) else None,
            "notes": str(row["Notes"]) if pd.notna(row["Notes"]) else None,
        }

        if category2:
            if category2 not in result[category1]:
                result[category1][category2] = {}
            result[category1][category2][str(row["ID"])] = achievement_data
        else:
            if "_achievements" not in result[category1]:
                result[category1]["_achievements"] = []
            result[category1]["_achievements"].append(achievement_data)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"Exported achievements to {json_path}")
    return result
