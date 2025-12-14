"""
src/recipe_helper.py
====================
Core recipe matching and suggestion logic for the Recipe Suggestion Helper CLI.

This module provides:
- Ingredient parsing and normalization
- Recipe matching with ingredient overlap counting
- Dietary preference filtering
- Recipe display formatting
- Ingredient substitution suggestions
- Recipe lookup by index or title

The recipe database is loaded from recipes.json on module import.
"""
import json
import os
from typing import List, Dict, Any, Tuple

# Load recipe database from JSON file in project root
BASE = os.path.dirname(os.path.dirname(__file__))
RECIPES_PATH = os.path.join(BASE, "recipes.json")

with open(RECIPES_PATH, "r", encoding="utf-8") as f:
    RECIPES = json.load(f)


def normalize(text: str) -> str:
    """Normalize text for case-insensitive matching.
    
    Args:
        text: Input string
        
    Returns:
        Lowercased and whitespace-stripped string
    """
    return text.lower().strip()


# Build set of all known ingredients from recipe database
def _get_valid_ingredients() -> set:
    """Extract all ingredients from recipe database for validation."""
    valid = set()
    for recipe in RECIPES:
        for ing in recipe.get("ingredients", []):
            valid.add(normalize(ing))
    return valid


VALID_INGREDIENTS = _get_valid_ingredients()


def parse_ingredients(text: str) -> List[str]:
    """Parse comma or semicolon-separated ingredient input into normalized list.
    
    Handles:
    - "chicken, rice, broccoli"
    - "tofu; bell pepper; soy sauce"
    - Mixed separators and extra spaces
    
    Args:
        text: Raw user input string
        
    Returns:
        List of normalized ingredients
    """
    import re

    # Split on commas or semicolons first (preferred explicit separators)
    parts = [p.strip() for p in re.split(r"[;,]", text) if p.strip()]

    # If user didn't use commas/semicolons and provided a space-separated list
    # (e.g. `chicken rice broccoli`), split on whitespace as a fallback.
    if len(parts) == 1 and " " in text and "," not in text and ";" not in text:
        parts = [p.strip() for p in text.split() if p.strip()]

    normalized = [normalize(p) for p in parts]
    return normalized


def match_recipes(ingredients: List[str], min_match: int = 2, diet: str = None) -> List[Tuple[Dict[str, Any], int]]:
    """Find recipes matching user ingredients with optional dietary filtering.
    
    Algorithm:
    1. Filter recipes by diet (if specified)
    2. Count matching ingredients per recipe (intersection of ingredient sets)
    3. Keep only recipes with >= min_match matching ingredients
    4. Sort by match count (descending) then title (ascending)
    
    Args:
        ingredients: List of user ingredients
        min_match: Minimum required ingredient matches (default: 2)
        diet: Optional dietary filter string (e.g., "vegan", "halal")
        
    Returns:
        List of (recipe_dict, match_count) tuples, sorted by best matches
    """
    # Normalize user-provided ingredients
    ing_set = set([normalize(i) for i in ingredients])
    matches = []
    
    for r in RECIPES:
        # Apply dietary filter if specified
        if diet:
            diets = [normalize(d) for d in r.get("diets", [])]
            if normalize(diet) not in diets:
                continue  # Skip recipes that don't match user's diet
        
        # Count ingredient overlap
        recipe_ings_list = [normalize(i) for i in r.get("ingredients", [])]

        # Allow substring and exact matches: e.g., user 'soba' matches 'soba noodles'
        matched = set()
        for u in ing_set:
            for ri in recipe_ings_list:
                if u == ri or u in ri or ri in u:
                    matched.add(ri)

        count = len(matched)
        
        # Keep recipe if it meets minimum threshold
        if count >= min_match:
            matches.append((r, count))
    
    # Sort: most matches first, then alphabetical
    matches.sort(key=lambda x: (-x[1], x[0]["title"]))
    return matches


def explain_recipe(recipe: Dict[str, Any]) -> str:
    """Format recipe for display to user.
    
    Includes:
    - Recipe title and time
    - Dietary tags
    - Numbered step-by-step instructions
    
    Args:
        recipe: Recipe dictionary with title, time, diets, steps
        
    Returns:
        Formatted multi-line string ready to print
    """
    lines = []
    lines.append(f"{recipe.get('title')} ({recipe.get('time', 'N/A')})")
    
    if recipe.get("diets"):
        lines.append(f"Dietary tags: {', '.join(recipe.get('diets'))}")
    
    lines.append("")  # Blank line for readability
    
    steps = recipe.get("steps", [])
    for i, s in enumerate(steps, 1):
        lines.append(f"- Step {i}: {s}")
    
    return "\n".join(lines)


# Ingredient substitution map for handling "I don't have X" questions
# Each entry: missing_ingredient -> suggested_alternative
# Includes culturally-appropriate swaps (e.g., tofu/lentils for meat)
SUBSTITUTIONS = {
    "butter": "oil or margarine",
    "milk": "plant milk (almond, soy, oat) or water",
    "egg": "mashed banana, applesauce (for baking), or flax egg (1 tbsp flaxseed + 3 tbsp water)",
    "eggs": "mashed banana, applesauce (for baking), or flax egg (1 tbsp flaxseed + 3 tbsp water per egg)",
    "sour cream": "plain yogurt or greek yogurt",
    "cream": "milk with butter, or coconut cream",
    "heavy cream": "half-and-half with butter, or coconut cream",
    "broth": "water + bouillon cube, or water + soy sauce",
    "chicken broth": "vegetable broth or water + seasoning",
    "beef broth": "mushroom broth or vegetable broth",
    "chicken": "tofu, tempeh, chickpeas, or seitan",
    "beef": "lentils, mushrooms, or textured vegetable protein (TVP)",
    "pork": "tofu, tempeh, or mushrooms",
    "fish": "tofu, hearts of palm, or white beans",
    "shrimp": "hearts of palm or chickpeas",
    "bacon": "coconut bacon, tempeh bacon, or smoked paprika",
    "cheese": "nutritional yeast, cashew cream, or vegan cheese",
    "parmesan": "nutritional yeast or vegan parmesan",
    "yogurt": "coconut yogurt, soy yogurt, or sour cream",
    "sugar": "honey, maple syrup, or coconut sugar",
    "brown sugar": "white sugar + molasses, or coconut sugar",
    "flour": "all-purpose flour, whole wheat flour, or gluten-free flour blend",
    "bread crumbs": "crushed crackers, panko, or rolled oats",
    "mayonnaise": "greek yogurt, sour cream, or avocado",
    "soy sauce": "tamari (gluten-free) or coconut aminos",
    "wine": "broth + vinegar, or grape juice",
    "vinegar": "lemon juice or lime juice",
    "lemon juice": "vinegar or lime juice",
    "garlic": "garlic powder (1/8 tsp per clove) or shallots",
    "onion": "shallots, leeks, or onion powder",
    "tomato paste": "ketchup or tomato sauce (reduce liquid)",
    "cornstarch": "flour (use 2x amount) or arrowroot powder",
    "baking powder": "1/4 tsp baking soda + 1/2 tsp cream of tartar",
    "buttermilk": "milk + 1 tbsp vinegar or lemon juice (let sit 5 min)",
    "honey": "maple syrup, agave nectar, or sugar",
    "maple syrup": "honey, agave nectar, or corn syrup",
    "olive oil": "vegetable oil, canola oil, or avocado oil",
    "vegetable oil": "canola oil, olive oil, or melted butter",
    "coconut milk": "regular milk with coconut extract, or cashew cream",
    "ginger": "ground ginger (1/4 tsp per 1 tbsp fresh)",
    "cilantro": "parsley or culantro",
    "parsley": "cilantro or basil",
    "basil": "oregano or thyme",
}


def suggest_substitute(ingredient: str) -> str:
    """Suggest an alternative ingredient with smart matching.
    
    Args:
        ingredient: Missing ingredient name
        
    Returns:
        Suggestion string or "I don't have a suggestion for that ingredient"
    """
    k = normalize(ingredient)
    
    # Direct match
    if k in SUBSTITUTIONS:
        return f"Try using: {SUBSTITUTIONS[k]}"
    
    # Try removing common suffixes for plural handling
    if k.endswith('s') and k[:-1] in SUBSTITUTIONS:
        return f"Try using: {SUBSTITUTIONS[k[:-1]]}"
    
    # Try adding 's' for plural match
    if k + 's' in SUBSTITUTIONS:
        return f"Try using: {SUBSTITUTIONS[k + 's']}"
    
    # Partial match - find ingredients that contain or are contained in the query
    for key, value in SUBSTITUTIONS.items():
        if k in key or key in k:
            return f"Try using: {value}"
    
    # No match found
    return f"I don't have a suggestion for '{ingredient}'. Try searching online for '{ingredient} substitute'"


def find_recipe_by_title_or_index(query: str) -> Dict[str, Any]:
    """Look up a recipe by numeric index (1-based) or partial title match.
    
    Matching:
    - "1" matches RECIPES[0] (1-based for user convenience)
    - "stir" matches "Tofu Stir-Fry" (case-insensitive substring)
    
    Args:
        query: Either a number string or recipe title (partial)
        
    Returns:
        Recipe dict if found, empty dict otherwise
    """
    q = normalize(query)
    
    # Try numeric index (1-based for user-friendly UX)
    if q.isdigit():
        idx = int(q) - 1
        if 0 <= idx < len(RECIPES):
            return RECIPES[idx]
    
    # Try partial title match
    for r in RECIPES:
        if q in normalize(r.get("title", "")):
            return r
    
    return {}


def get_available_diets() -> List[str]:
    """Get all dietary categories available in recipe database.
    
    Returns:
        Sorted list of unique diet tags (e.g., ["halal", "kosher", "vegan", ...])
    """
    diets = set()
    for r in RECIPES:
        diets.update(r.get("diets", []))
    return sorted(list(diets))


def validate_ingredients(ingredients: List[str]) -> Tuple[List[str], List[str]]:
    """Validate user ingredients against known ingredients in database.
    
    Performs substring matching to catch variations (e.g., "soba" matches "soba noodles").
    
    Args:
        ingredients: List of user-provided ingredients
        
    Returns:
        Tuple of (valid_ingredients, invalid_ingredients)
    """
    valid = []
    invalid = []
    
    for ing in ingredients:
        ing_norm = normalize(ing)
        # Check for exact match or substring match
        found = False
        for known_ing in VALID_INGREDIENTS:
            if ing_norm == known_ing or ing_norm in known_ing or known_ing in ing_norm:
                valid.append(ing)
                found = True
                break
        
        if not found:
            invalid.append(ing)
    
    return valid, invalid

