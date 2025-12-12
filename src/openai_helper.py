"""openai_helper.py
Wrapper around the OpenAI Python client for richer cooking assistance.

This module provides:
- ask_openai(): Answer free-form questions about a recipe
- generate_recipes_from_ingredients(): Generate full recipes from user ingredients
"""
import os
import json
from typing import Optional, Dict, Any, List

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


def ask_openai(question: str, recipe: Dict[str, Any], system_prompt: Optional[str] = None, model: str = "gpt-4o-mini") -> Optional[str]:
    """Ask OpenAI for a richer, contextual answer about a recipe.

    Args:
        question: User's free-form question
        recipe: The selected recipe dictionary (title, ingredients, steps, time, diets)
        system_prompt: Optional system prompt to guide the model
        model: Model name to use (default: compact GPT-4o-mini)

    Returns:
        Answer text when successful, or None when API key/library is missing or on error.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return None

    # Initialize OpenAI client with API key
    client = OpenAI(api_key=api_key)

    # Build a compact context for the model
    context = []
    sys_p = system_prompt or (
        "You are a helpful cooking assistant. Answer concisely and use numbered steps when describing actions."
    )
    context.append({"role": "system", "content": sys_p})

    # Add recipe summary as context
    recipe_summary = f"Title: {recipe.get('title')}\nTime: {recipe.get('time')}\nIngredients: {', '.join(recipe.get('ingredients', []))}\nSteps: {' | '.join(recipe.get('steps', []))}"
    context.append({"role": "user", "content": f"Recipe context:\n{recipe_summary}"})
    context.append({"role": "user", "content": f"User question: {question}"})
    
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=context,
            max_tokens=500,
            temperature=0.6,
        )
        # Extract answer
        if resp.choices and len(resp.choices) > 0:
            text = resp.choices[0].message.content
            return text.strip() if text else None
        return None
    except Exception:
        return None


def generate_recipes_from_ingredients(
    ingredients: List[str],
    diet: Optional[str] = None,
    meal_type: Optional[str] = None,
    model: str = "gpt-4o-mini"
) -> Optional[List[Dict[str, Any]]]:
    """Generate 3-5 complete recipes from user ingredients using OpenAI.
    
    Args:
        ingredients: List of user ingredients (e.g., ["chicken", "rice", "broccoli"])
        diet: Optional dietary filter (e.g., "vegan", "halal", "kosher")
        meal_type: Optional meal type (e.g., "breakfast", "lunch", "dinner", "snack")
        model: Model to use (default: gpt-4o-mini)
    
    Returns:
        List of recipe dicts with title, ingredients, steps, time, diets, allergens, nutrition
        or None if API key missing/error occurs.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return None
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Build the prompt for recipe generation
        ing_str = ", ".join(ingredients)
        constraints = []
        if diet:
            constraints.append(f"must be {diet}")
        if meal_type:
            constraints.append(f"suitable for {meal_type}")
        constraint_str = " and ".join(constraints) if constraints else ""
        
        prompt = f"""Generate 3-5 complete recipes using these ingredients: {ing_str}
{f'Constraints: {constraint_str}' if constraint_str else ''}

Return ONLY a valid JSON array with no additional text. Each recipe must have this exact structure:
[
  {{
    "title": "Recipe Name",
    "ingredients": ["ingredient 1", "ingredient 2", ...],
    "steps": ["Step 1 description", "Step 2 description", ...],
    "time": "15 minutes",
    "diets": ["vegan", "kosher"],
    "allergens": ["soy", "gluten"],
    "nutrition": {{
      "calories": 300,
      "protein_g": 25,
      "carbs_g": 35,
      "fat_g": 10
    }}
  }}
]

Ensure:
1. All recipes use the provided ingredients
2. Each recipe has 3-6 clear steps
3. Times are realistic (10-60 minutes)
4. Allergens are accurate guesses based on common allergens
5. Nutrition is a reasonable estimate
6. diets array lists applicable dietary categories (vegan, vegetarian, halal, kosher, pescatarian, etc.)
"""
        
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional chef and nutritionist. Generate practical recipes in valid JSON format. Return ONLY the JSON array, no other text."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7,
            timeout=15,
        )
        
        if not resp.choices or len(resp.choices) == 0:
            return None
        
        response_text = resp.choices[0].message.content.strip()
        
        # Try to parse JSON from the response
        try:
            recipes = json.loads(response_text)
            if isinstance(recipes, list) and len(recipes) > 0:
                return recipes
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from the text
            import re
            match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if match:
                try:
                    recipes = json.loads(match.group())
                    if isinstance(recipes, list) and len(recipes) > 0:
                        return recipes
                except json.JSONDecodeError:
                    pass
        
        return None
        
    except Exception:
        return None
