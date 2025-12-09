#!/usr/bin/env python3
"""
Run: python main.py

This is the entrypoint for the Recipe Suggestion Helper CLI.
"""
from src.recipe_helper import parse_ingredients, match_recipes, explain_recipe, suggest_substitute, get_available_diets
import os
import sys


def ask_user(prompt: str) -> str:
    return input(prompt + "\n> ").strip()


def main():
    print("Hi! I'm your Recipe Suggestion Helper.")
    print()
    
    # Ask about dietary preferences
    available_diets = get_available_diets()
    print(f"Available dietary options: {', '.join(available_diets)}")
    diet_choice = ask_user("Do you have any dietary preferences? (or press Enter to skip)")
    diet_filter = diet_choice.strip() if diet_choice.strip() else None
    
    print()
    print("Tell me what ingredients you have (comma-separated). Example: 'chicken, rice, broccoli'")
    ing_text = ask_user("What ingredients do you have?")
    ingredients = parse_ingredients(ing_text)
    if not ingredients:
        print("I didn't hear any ingredients. Exiting.")
        sys.exit(0)

    matches = match_recipes(ingredients, min_match=2, diet=diet_filter)
    if not matches:
        print("Sorry, I couldn't find recipes matching at least 2 of your ingredients")
        if diet_filter:
            print(f"with the '{diet_filter}' dietary requirement.")
        print("Try adding more ingredients or removing dietary filters.")
        sys.exit(0)

    print("Great! Here are some recipes you can make:")
    for i, (r, count) in enumerate(matches[:3], 1):
        diets_str = f" — {', '.join(r.get('diets', []))}" if r.get('diets') else ""
        print(f"{i}. {r.get('title')} ({r.get('time')}){diets_str} — matches {count} ingredient(s)")

    choice = ask_user("Which number would you like to know more about, or type a recipe name? (or 'no' to exit)")
    if choice.lower() in ('no', 'n', 'exit', 'quit'):
        print("Okay, bye!")
        return

    selected = None
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(matches[:3]):
            selected = matches[idx][0]
    if not selected:
        from src.recipe_helper import find_recipe_by_title_or_index
        r = find_recipe_by_title_or_index(choice)
        if r:
            selected = r

    if not selected:
        print("Couldn't find that selection. Exiting.")
        return

    print()
    print(explain_recipe(selected))
    print()

    while True:
        q = ask_user("Anything else? Ask for substitutions, time, or 'want to make this' to confirm, or 'exit'")
        if q.lower() in ("exit", "quit", "no"):
            print("Bye — happy cooking!")
            break
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
        print("Sorry — I can answer substitution and time questions. For richer answers, set OPENAI_API_KEY and use the main project with OpenAI integration.")


if __name__ == '__main__':
    main()
