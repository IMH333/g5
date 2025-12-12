#!/usr/bin/env python3
"""
Run: python main.py

This is the entrypoint for the Recipe Suggestion Helper CLI.
"""
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.recipe_helper import parse_ingredients, match_recipes, explain_recipe, suggest_substitute, get_available_diets
from src.openai_helper import ask_openai, generate_recipes_from_ingredients
import os
import sys
import json
import re
from datetime import datetime
from rich import print 


def _safe_filename(title: str) -> str:
    # make a simple safe filename from title
    return re.sub(r"[^0-9a-zA-Z_-]", "_", title).strip("_")


def ask_user(prompt: str) -> str:
    return input(prompt + "\n> ").strip()


def _mask_key(key: str) -> str:
    if not key:
        return ""
    if len(key) <= 8:
        return key[0] + "*" * (len(key) - 1)
    return f"{key[:4]}" + "*" * (len(key) - 8) + f"{key[-4:]}"


def _get_arg_value(args, flag: str, default: int) -> int:
    """Parse integer CLI flag values like --max-results=5 or --max=5."""
    for a in args:
        if a.startswith(flag + "="):
            try:
                return int(a.split("=", 1)[1])
            except ValueError:
                return default
    return default


def main():
    # support quick check: `python main.py --show-key`
    if "--show-key" in sys.argv:
        key = os.getenv("GROQ_API_KEY")
        if key:
            print(f"GROQ_API_KEY={_mask_key(key)}")
        else:
            print("GROQ_API_KEY is not set")
        return

    max_results = _get_arg_value(sys.argv, "--max-results", default=5)
    max_results = _get_arg_value(sys.argv, "--max", default=max_results)
    allow_ai = "--no-ai" not in sys.argv

    print("[bold underline blue]Hi! I'm your Recipe Suggestion Helper.[/bold underline blue]")
    print()

    # Ask about meal type
    available_meal_types = ["breakfast", "snack", "lunch", "dinner"]
    print(f"[cyan]Available meal types: {', '.join(available_meal_types)}[/cyan]")
    meal_choice = ask_user("What type of meal is this? (or press Enter to skip)")
    meal_type = meal_choice.strip() if meal_choice.strip() else None
    print()
    
    # Ask about dietary preferences
    available_diets = get_available_diets()
    print(f"[cyan]Available dietary options: {', '.join(available_diets)}[/cyan]")
    diet_choice = ask_user("Do you have any dietary preferences? (or press Enter to skip)")
    diet_filter = diet_choice.strip() if diet_choice.strip() else None
    
    print()
    print("[cyan]Tell me what ingredients you have (comma-separated). Example: 'chicken, rice, broccoli'[/cyan]")
    ing_text = ask_user("What ingredients do you have?")
    ingredients = parse_ingredients(ing_text)
    if not ingredients:
        print("[pink1]I didn't hear any ingredients. Exiting.[/pink1]")
        sys.exit(0)

    # Local recipe matches first
    matches = match_recipes(ingredients, min_match=2, diet=diet_filter)
    options = [(r, count, "local") for r, count in matches[:max_results]]

    # If we need more options, auto-generate with OpenAI (if allowed and key present)
    if allow_ai and len(options) < max_results:
        print(f"[yellow]Generating {max_results - len(options)} more recipe(s)...[/yellow]")
        print("[dim](This may take a few seconds, especially during high API usage)[/dim]")
        ai_recipes = generate_recipes_from_ingredients(
            ingredients=ingredients,
            diet=diet_filter,
            meal_type=meal_type,
        )
        if ai_recipes:
            print(f"[green]✓ Generated {len(ai_recipes)} recipe(s)[/green]")
            for r in ai_recipes:
                options.append((r, None, "ai"))
                if len(options) >= max_results:
                    break
        else:
            print("[pink1]⚠ Recipe generation was unavailable.[/pink1]")
            print("[dim]This may be due to rate limits or network issues. Showing local matches only.[/dim]")

    if not options:
        print("[pink1]Sorry, I couldn't find recipes matching at least 2 of your ingredients[/pink1]")
        if diet_filter:
            print(f"[pink1]with the '{diet_filter}' dietary requirement.[/pink1]")
        if allow_ai:
            print("[cyan]Try again with AI generation enabled and a valid GROQ_API_KEY.[/cyan]")
        else:
            print("[cyan]Try adding more ingredients or removing dietary filters.[/cyan]")
        sys.exit(0)

    print(f"[cyan]Great! Here are up to {len(options)} recipe options:[/cyan]")
    for i, (r, count, source) in enumerate(options, 1):
        diets_str = f" — {', '.join(r.get('diets', []))}" if r.get('diets') else ""
        match_note = f" — matches {count} ingredient(s)" if count is not None else ""
        src_note = "[AI]" if source == "ai" else "[local]"
        print(f"{i}. {r.get('title')} ({r.get('time', 'time n/a')}){diets_str} {src_note}{match_note}")

    choice = ask_user("Which number would you like to know more about, or type a recipe name? (or 'no' to exit)")
    if choice.lower() in ('no', 'n', 'exit', 'quit'):
        print("[pink1]Okay, bye![/pink1]")
        return

    selected = None
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(options):
            selected = options[idx][0]
    if not selected:
        from src.recipe_helper import find_recipe_by_title_or_index
        r = find_recipe_by_title_or_index(choice)
        if r:
            selected = r

    if not selected:
        print("[pink1]Couldn't find that selection. Exiting.[/pink1]")
        return

    print()
    print(explain_recipe(selected))

    # Display detected allergens (best-effort)
    allergens = selected.get("allergens", [])
    print()
    if allergens:
        print("[orange_red1]Allergens (best-effort): [/orange_red1]" + ", ".join(allergens))
    else:
        print("[orange_red1]Allergens (best-effort): None detected [/orange_red1]")
    print()

    # Display nutrition estimates (best-effort)
    nutrition = selected.get("nutrition", {})
    if nutrition:
        print(f"Nutrition estimate (per recipe): {nutrition.get('calories')} cal | {nutrition.get('protein_g')}g protein | {nutrition.get('carbs_g')}g carbs | {nutrition.get('fat_g')}g fat")
        print("(Best-effort estimate. Do not use for medical/diet purposes.)")
    else:
        print("Nutrition estimate: Not available")
    print()

    while True:
        try:
            q = ask_user("Anything else? Ask for substitutions, time, or 'want to make this' to confirm, or 'exit'")
        except (EOFError, KeyboardInterrupt):
            print("[pink1]\nInput closed. Exiting.[/pink1]")
            break

        # If the user just pressed Enter (empty response), reprompt instead
        if not q:
            continue

        if q.lower() in ("exit", "quit", "no"):
            print("Bye — happy cooking!")
            break
        # New: handle confirmation flow
        if "want to make this" in q.lower() or q.lower().strip() == "want to make this":
            # Show shopping list vs available ingredients
            have = [i.lower() for i in ingredients]
            recipe_ings = selected.get("ingredients", [])
            missing = [ing for ing in recipe_ings if ing.lower() not in have]
            print("\nGreat — preparing this recipe for you.")
            print("Shopping list:")
            for ing in recipe_ings:
                mark = "(have)" if ing.lower() in have else "(missing)"
                print(f" - {ing} {mark}")

            # Estimate cost (very rough heuristic)
            est_cost = round(len(recipe_ings) * 1.75, 2)
            print(f"Estimated cost (rough): ${est_cost}")

            # Offer to save recipe and write a printable recipe card
            save = ask_user("Save this recipe to your saved list and create a recipe card? (y/n)")
            if save.lower() in ("y", "yes"):
                saved_path = os.path.join("saved_recipes.json")
                try:
                    if os.path.exists(saved_path):
                        with open(saved_path, "r", encoding="utf-8") as f:
                            saved = json.load(f)
                    else:
                        saved = []
                except Exception:
                    saved = []
                entry = {"title": selected.get("title"), "saved_at": datetime.utcnow().isoformat(), "allergens": selected.get("allergens", [])}
                saved.append(entry)
                with open(saved_path, "w", encoding="utf-8") as f:
                    json.dump(saved, f, indent=2)
                # create a simple recipe card file
                card_dir = os.path.join("saved_cards")
                os.makedirs(card_dir, exist_ok=True)
                fname = _safe_filename(selected.get("title", "recipe")) + ".txt"
                card_path = os.path.join(card_dir, fname)
                with open(card_path, "w", encoding="utf-8") as f:
                    f.write(f"{selected.get('title')}\n")
                    f.write("Ingredients:\n")
                    for ing in recipe_ings:
                        f.write(f" - {ing}\n")
                    f.write("\nAllergens:\n")
                    if selected.get("allergens"):
                        for a in selected.get("allergens"):
                            f.write(f" - {a}\n")
                    else:
                        f.write(" - (none detected)\n")
                    f.write("\nSteps:\n")
                    for step in selected.get("steps", []):
                        f.write(f" - {step}\n")
                    f.write(f"\nTime: {selected.get('time')}\n")
                    f.write("\nNutrition (rough estimate):\n")
                    nutrition = selected.get("nutrition", {})
                    if nutrition:
                        f.write(f" - Calories: {nutrition.get('calories')}\n")
                        f.write(f" - Protein: {nutrition.get('protein_g')}g\n")
                        f.write(f" - Carbs: {nutrition.get('carbs_g')}g\n")
                        f.write(f" - Fat: {nutrition.get('fat_g')}g\n")
                    f.write("\n(Nutrition estimates are best-effort and should NOT be used for medical/diet purposes.)\n")
                print(f"Saved to {saved_path} and created recipe card at {card_path}")

            # Timers suggestion based on recipe time
            t = selected.get("time", "")
            m = re.search(r"(\d+)", t)
            if m:
                total = int(m.group(1))
                prep = max(5, total // 4)
                cook = max(5, total - prep)
                print(f"Suggested timers: prep ~{prep} minutes, cook ~{cook} minutes (total {total} minutes)")
            else:
                print("Suggested timers: prep ~10 minutes, cook ~15 minutes")
            continue
        if "i don't have" in q.lower() or "dont have" in q.lower():
            part = q.lower().split("have", 1)[-1].strip()
            sub = suggest_substitute(part)
            print(sub)
            continue
        # For now we use the simple built-in responder in recipe_helper for basic questions
        # (openai integration can be added later)
        if "time" in q.lower() or "how long" in q.lower():
            print(f"This recipe takes about {selected.get('time')}")
            continue
        if "steps" in q.lower() or "how do i" in q.lower():
            print(explain_recipe(selected))
            continue
        # Try OpenAI for richer free-form follow-ups when configured
        openai_answer = None
        try:
            openai_answer = ask_openai(q, selected)
        except Exception:
            openai_answer = None

        if openai_answer:
            print(openai_answer)
            continue

        print("Sorry — I can answer substitution and time questions. For richer answers, set GROQ_API_KEY and run again.")


if __name__ == '__main__':
    main()
