#!/usr/bin/env python3
"""
Add allergen flags to recipes.json using a best-effort keyword mapping.

Run: python3 scripts/add_allergen_flags.py
This updates `recipes.json` in place and prints a short report.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RPATH = BASE / "recipes.json"

ALLERGEN_MAP = {
    "milk": [
        "milk", "butter", "cream", "yogurt", "cheese", "parmesan", "feta", "mozzarella",
        "buttermilk", "ghee", "evaporated milk", "condensed milk", "goat milk", "sheep milk"
    ],
    "egg": ["egg", "egg white", "egg yolk", "mayonnaise"],
    "soy": [
        "soy", "tofu", "soy sauce", "tempeh", "edamame", "miso", "natto", "soybean",
        "soy lecithin"
    ],
    "peanut": ["peanut", "peanut butter", "peanut oil"],
    "tree_nuts": [
        "almond", "walnut", "pecan", "cashew", "hazelnut", "macadamia", "pistachio",
        "brazil nut", "brazilnut", "chestnut", "pine nut", "pine nuts"
    ],
    "wheat_gluten": [
        "flour", "wheat", "pasta", "bread", "tortilla", "breadcrumbs", "semolina", "spelt",
        "rye", "barley", "bulgur", "farro", "kamut", "noodles", "ramen"
    ],
    "fish": [
        "fish", "salmon", "tuna", "cod", "halibut", "trout", "anchovy", "mackerel", "herring"
    ],
    "shellfish": [
        "shrimp", "prawn", "prawns", "scallop", "mussel", "mussels", "oyster", "crab", "lobster"
    ],
    "sesame": ["sesame", "sesame seeds", "tahini", "sesame oil"],
    "mustard": ["mustard", "mustard seed", "mustard powder"],
    "celery": ["celery", "celeriac"],
    "sulfites": ["sulfite", "sulphite", "sulphites", "sulfites", "dried fruit"],
}

def detect_allergens(ingredients):
    found = set()
    low = [i.lower() for i in ingredients]
    for allergen, keywords in ALLERGEN_MAP.items():
        for kw in keywords:
            for ing in low:
                if kw in ing:
                    found.add(allergen)
    return sorted(list(found))

def main():
    if not RPATH.exists():
        print("recipes.json not found; aborting")
        return
    with open(RPATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for r in data:
        ingredients = r.get("ingredients", [])
        allergens = detect_allergens(ingredients)
        if allergens:
            r["allergens"] = allergens
        else:
            # Ensure key exists as empty list for clarity
            r.setdefault("allergens", [])
        updated += 1

    # Write back (overwrite)
    with open(RPATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Short report
    counts = {}
    for r in data:
        for a in r.get("allergens", []):
            counts[a] = counts.get(a, 0) + 1

    print(f"Updated {len(data)} recipes with 'allergens' field (best-effort tagging).")
    if counts:
        print("Allergen counts:")
        for a, c in sorted(counts.items(), key=lambda x: -x[1]):
            print(f" - {a}: {c}")
    else:
        print("No allergens detected (unexpected).")

if __name__ == '__main__':
    main()
