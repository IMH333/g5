import json
import os
from typing import List, Dict, Any, Tuple

BASE = os.path.dirname(os.path.dirname(__file__))
RECIPES_PATH = os.path.join(BASE, "recipes.json")

with open(RECIPES_PATH, "r", encoding="utf-8") as f:
    RECIPES = json.load(f)


def normalize(text: str) -> str:
    return text.lower().strip()


def parse_ingredients(text: str) -> List[str]:
    # split by comma or space and normalize
    parts = [p.strip() for p in text.replace(';', ',').split(',') if p.strip()]
    normalized = [normalize(p) for p in parts]
    return normalized


def match_recipes(ingredients: List[str], min_match: int = 2, diet: str = None) -> List[Tuple[Dict[str, Any], int]]:
    """Return list of (recipe, match_count) sorted by best matches.
    Only recipes with match_count >= min_match are returned.
    If diet is specified, filter to recipes with that diet tag.
    """
    ing_set = set([normalize(i) for i in ingredients])
    matches = []
    for r in RECIPES:
        # Check diet filter
        if diet:
            diets = [normalize(d) for d in r.get("diets", [])]
            if normalize(diet) not in diets:
                continue
        
        recipe_ings = set([normalize(i) for i in r.get("ingredients", [])])
        common = ing_set & recipe_ings
        count = len(common)
        if count >= min_match:
            matches.append((r, count))
    matches.sort(key=lambda x: (-x[1], x[0]["title"]))
    return matches


def explain_recipe(recipe: Dict[str, Any]) -> str:
    lines = []
    lines.append(f"{recipe.get('title')} ({recipe.get('time', 'N/A')})")
    if recipe.get("diets"):
        lines.append(f"Dietary tags: {', '.join(recipe.get('diets'))}")
    lines.append("")
    steps = recipe.get("steps", [])
    for i, s in enumerate(steps, 1):
        lines.append(f"- Step {i}: {s}")
    return "\n".join(lines)


# Simple substitution hints
SUBSTITUTIONS = {
    "butter": "oil",
    "milk": "plant milk or water",
    "egg": "mashed banana or applesauce (for baking)",
    "sour cream": "yogurt",
    "cream": "milk",
    "broth": "water + seasoning",
    "chicken": "tofu or chickpeas",
    "beef": "lentils or mushrooms",
    "fish": "tofu or beans",
}


def suggest_substitute(ingredient: str) -> str:
    k = normalize(ingredient)
    return SUBSTITUTIONS.get(k, "I don't have a suggestion for that ingredient")


def find_recipe_by_title_or_index(query: str) -> Dict[str, Any]:
    q = normalize(query)
    # try index like '1' or '1.'
    if q.isdigit():
        idx = int(q) - 1
        if 0 <= idx < len(RECIPES):
            return RECIPES[idx]
    # match by title contains
    for r in RECIPES:
        if q in normalize(r.get("title", "")):
            return r
    return {}


def get_available_diets() -> List[str]:
    """Return list of unique diets available across all recipes."""
    diets = set()
    for r in RECIPES:
        diets.update(r.get("diets", []))
    return sorted(list(diets))
