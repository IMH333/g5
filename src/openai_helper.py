"""openai_helper.py
Wrapper around the Groq API for fast, free cooking assistance.

This module provides:
- ask_openai(): Answer free-form questions about a recipe (uses Groq)
- generate_recipes_from_ingredients(): Generate full recipes from user ingredients (uses Groq)

Note: Despite the filename, this now uses Groq API for fast, free inference.
"""
import os
import json
import time
from typing import Optional, Dict, Any, List

try:
    from groq import Groq, RateLimitError, APIError
except Exception:
    Groq = None
    RateLimitError = None
    APIError = None


def _retry_with_backoff(func, max_retries=3, initial_delay=1.0):
    """Retry a function with exponential backoff for rate limit errors.
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds (doubles each retry)
        
    Returns:
        Function result or None on failure
    """
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            error_name = type(e).__name__
            
            # Check if it's a rate limit error
            if RateLimitError and isinstance(e, RateLimitError):
                if attempt < max_retries - 1:
                    import sys
                    print(f"[Debug] Rate limit hit. Retrying in {delay}s... (attempt {attempt + 1}/{max_retries})", file=sys.stderr)
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                    continue
                else:
                    import sys
                    print(f"[Debug] Rate limit exceeded after {max_retries} retries", file=sys.stderr)
                    return None
            
            # For other errors, don't retry
            import sys
            print(f"[Debug] OpenAI error: {error_name}", file=sys.stderr)
            return None
    
    return None


def ask_openai(question: str, recipe: Dict[str, Any], system_prompt: Optional[str] = None, model: str = "llama-3.3-70b-versatile") -> Optional[str]:
    """Ask Groq (fast Llama model) for a richer, contextual answer about a recipe.

    Args:
        question: User's free-form question
        recipe: The selected recipe dictionary (title, ingredients, steps, time, diets)
        system_prompt: Optional system prompt to guide the model
        model: Model name to use (default: Llama 3.3 70B)

    Returns:
        Answer text when successful, or None when API key/library is missing or on error.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or Groq is None:
        return None

    # Initialize Groq client with API key
    try:
        client = Groq(api_key=api_key)
    except Exception:
        return None

    # Build context for the model
    sys_p = system_prompt or (
        "You are a helpful cooking assistant. Answer concisely and use numbered steps when describing actions."
    )

    # Add recipe summary as context
    recipe_summary = f"Title: {recipe.get('title')}\nTime: {recipe.get('time')}\nIngredients: {', '.join(recipe.get('ingredients', []))}\nSteps: {' | '.join(recipe.get('steps', []))}"
    
    def _make_request():
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": sys_p},
                {"role": "user", "content": f"Recipe context:\n{recipe_summary}\n\nUser question: {question}"}
            ],
            max_tokens=500,
            temperature=0.6,
            timeout=10,

        )
        if response.choices and len(response.choices) > 0:
            text = response.choices[0].message.content
            return text.strip() if text else None
        return None
    
    return _retry_with_backoff(_make_request, max_retries=3, initial_delay=1.0)


def generate_recipes_from_ingredients(
    ingredients: List[str],
    diet: Optional[str] = None,
    meal_type: Optional[str] = None,
    model: str = "llama-3.3-70b-versatile"
) -> Optional[List[Dict[str, Any]]]:
    """Generate 3-5 complete recipes from user ingredients using Groq (fast & free).
    
    Args:
        ingredients: List of user ingredients (e.g., ["chicken", "rice", "broccoli"])
        diet: Optional dietary filter (e.g., "vegan", "halal", "kosher")
        meal_type: Optional meal type (e.g., "breakfast", "lunch", "dinner", "snack")
        model: Model to use (default: Llama 3.3 70B - fast and capable)
    
    Returns:
        List of recipe dicts with title, ingredients, steps, time, diets, allergens, nutrition
        or None if API key missing/error occurs.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or Groq is None:
        return None
    
    try:
        client = Groq(api_key=api_key)
    except Exception:
        return None
        
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
    
    def _make_request():
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional chef and nutritionist. Generate practical recipes in valid JSON format. Return ONLY the JSON array, no other text."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.7,
            timeout=10,
        )
        
        if not response.choices or len(response.choices) == 0:
            return None
        
        response_text = response.choices[0].message.content.strip()
        
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
    
    return _retry_with_backoff(_make_request, max_retries=3, initial_delay=2.0)
