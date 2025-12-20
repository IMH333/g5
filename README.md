# Recipe Suggestion Helper – CLI AI Chatbot
**AIEG F25 Capstone Project**

## 🎯 Quick Pitch // Quick Start
A conversational CLI chatbot that helps users solve the universal issue of "What should I eat?!" Recipes are based on ingredients they have at home. Users will enter 3 or more ingredients, get 2–3 suggestions, and ask follow-up questions about preparation, cooking time, and ingredient substitutions.  The recipes can also be catered to certain allergies or dietary restrictions.
Getting started is easier than ever - simply run the file on the terminal with "python main.py" and follow the prompts.

---

## ✨ Features

### Core Functionality
- **Ingredient-Based Matching** – Type ingredients → get matching recipes (minimum 2 ingredients matched)
- **Dietary Filters** – Support for vegan, vegetarian, pescatarian, halal, and kosher diets
- **Recipe Details** – Step-by-step cooking instructions with prep times
- **Smart Substitutions** – Suggest alternatives for ingredients you don't have
- **Natural Conversation** – Handles 4–5 intent types (list ingredients, get suggestions, explain recipe, ask questions, exit)
- **Graceful Error Handling** – Friendly messages for unclear input or no matches

### Intent Recognition
1. **List Ingredients** – User provides pantry items
2. **Get Suggestions** – Bot returns matching recipes
3. **Explain Recipe** – Detailed steps for selected recipe
4. **Ask Questions** – Handle substitutions, time estimates, dietary queries
5. **Exit** – Graceful farewell and session end

---

## 🚀 Quickstart

### Prerequisites
- Python 3.8+
- Groq API key integrated within .env file but hidden from public.

### Installation

```bash
# Clone the repository
git clone https://github.com/davvvidk03/g5.git
cd g5

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Run the CLI

```bash
python main.py
```

**Example Conversation:**
```
Hi! I'm your Recipe Helper.

What type of meal is this? (breakfast, snack, lunch, dinner)
> dinner

Available dietary options: halal, kosher, pescatarian, vegan, vegetarian
Do you have any dietary preferences? (or press Enter to skip)
> vegan

Tell me what ingredients you have (comma-separated). Example: 'chicken, rice, broccoli'
What ingredients do you have?
> tofu, broccoli, garlic

Great! Here are some recipes you can make:
1. Tofu Stir-Fry (20 minutes) — vegan, vegetarian — matches 3 ingredient(s)
2. Lentil & Vegetable Curry (30 minutes) — vegan, vegetarian — matches 2 ingredient(s)

Which number would you like to know more about, or type a recipe name? (or 'no' to exit)
> 1

Tofu Stir-Fry (20 minutes)
Dietary tags: vegan, vegetarian

- Step 1: Press tofu and cut into cubes.
- Step 2: Pan-fry tofu until golden, set aside.
- Step 3: Stir-fry veggies and garlic, add tofu back with soy sauce, cook until done.

Anything else? Ask for substitutions, time, or 'want to make this' to confirm, or 'exit'
> How long does it take?
This recipe takes about 20 minutes
> exit
Bye — happy cooking!
```

---

## 📦 Project Structure

```
g5/
├── main.py                  # CLI entrypoint (user interaction loop)
├── src/
│   └── recipe_helper.py     # Core logic (matching, filtering, substitutions)
├── recipes.json             # Recipe database (~13 recipes with dietary tags)
├── BACKLOG.md               # Sprint backlog (18 tasks)
├── BACKLOG.csv              # CSV export for GitHub Projects
├── scripts/
│   └── create_issues.sh     # Script to auto-create GitHub Issues from CSV
├── README.md                # This file
├── DEMO.md                  # Demo walkthrough and intent examples
├── ETHICS.md                # Privacy, bias, and risk assessment
└── requirements.txt         # Dependencies (currently none required)
```

---

## 🏗️ Architecture

### Data Flow Diagram
```
┌─────────────┐
│   User      │
│ Input (CLI) │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│  main.py (Interaction Loop) │
│  - Prompt for diet          │
│  - Collect ingredients      │
│  - Route to recipe_helper   │
└──────┬──────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│  src/recipe_helper.py (Logic)    │
│  - parse_ingredients()           │
│  - match_recipes()               │
│  - explain_recipe()              │
│  - suggest_substitute()          │
└──────┬───────────────────────────┘
       │
       ▼
┌─────────────────────┐
│  recipes.json       │
│  (13 recipes with   │
│   dietary tags)     │
└─────────────────────┘
```

### Conversation Flow
```
Start
  │
  ├─→ Ask: Diet preference?
  │     (Vegan / Vegetarian / Pescatarian / Halal / Kosher / Skip)
  │
  ├─→ Ask: What ingredients?
  │     (Parse comma-separated input)
  │
  ├─→ Match recipes (≥2 matching ingredients + diet filter)
  │     │
  │     ├─→ [Found matches] → Show top 3
  │     │                      │
  │     │                      ├─→ User selects recipe
  │     │                      │     │
  │     │                      │     ├─→ Show recipe details
  │     │                      │     │
  │     │                      │     ├─→ Ask: Anything else?
  │     │                      │     │     │
  │     │                      │     │     ├─→ [Time?] → Respond with time
  │     │                      │     │     ├─→ [Substitute?] → Suggest swap
  │     │                      │     │     ├─→ [Steps?] → Repeat recipe
  │     │                      │     │     └─→ [Exit] → Goodbye
  │     │                      │
  │     │                      └─→ [Back to start]
  │     │
  │     └─→ [No matches] → Try different ingredients
  │
  └─→ End (User exits)
```

---

## 💻 Code Quality

### Modular Design
- **`main.py`** – User interaction and CLI flow (47 lines)
- **`src/recipe_helper.py`** – Core algorithms and recipe logic (96 lines)
  - Recipe matching with configurable thresholds
  - Dietary filtering
  - Substitution hints
  - Utility functions for parsing and normalization
- **`recipes.json`** – Declarative recipe database (no hardcoding in code)

### Error Handling
- **Missing recipes** → Prompt user to try different ingredients
- **Invalid selection** → Re-ask user or exit gracefully
- **Empty input** → Politely ask again
- **No matches for diet** → Suggest trying without diet filter

### Documentation
- Inline docstrings in `recipe_helper.py`
- README with architecture diagrams
- DEMO.md with example intents
- ETHICS.md for responsible AI considerations

---

## 🧪 Testing

### Manual Test Cases (Happy Path)
1. ✅ **Vegan + tofu, broccoli** → Suggests Tofu Stir-Fry
2. ✅ **Halal + chicken, rice** → Suggests Chicken & Rice Bowl
3. ✅ **Pescatarian + fish, lemon** → Suggests Grilled Fish with Lemon
4. ✅ **No diet + multiple ingredients** → Shows diverse options
5. ✅ **Ask "How long does it take?"** → Returns recipe time
6. ✅ **Ask "Can I substitute butter?"** → Returns suggestion

### Edge Cases Covered
- Empty ingredient input → Exit gracefully
- No matching recipes → Suggest trying different ingredients
- Invalid recipe selection → Re-ask or exit
- Unrecognized questions → Suggest available features

---

## 🎬 Demo (4–6 Minutes)

See **[DEMO.md](DEMO.md)** for:
- Full walkthrough with sample inputs/outputs
- Intent classification examples
- Error handling demonstrations
- Q&A talking points for each team member

---

## 📋 Recipes Included (13 Total)

### Vegan (4)
- Tomato Pasta
- Tofu Stir-Fry
- Lentil & Vegetable Curry
- Quick Veggie Stir-Fry

### Vegetarian (6)
- Fried Rice
- Veggie Omelette
- Grilled Cheese
- Pancakes
- + all vegan options

### Pescatarian (2)
- Tuna Salad
- Grilled Fish with Lemon

### Halal / Kosher (7)
- Chicken & Rice Bowl
- Chicken Stir-Fry
- One-Pan Chicken & Veggies
- Tuna Salad
- Grilled Fish with Lemon
- Quick Veggie Stir-Fry
- (+ others)

---

## 🔐 Responsibility & Ethics

See **[ETHICS.md](ETHICS.md)** for:
- **Privacy** – No user data is logged or stored unless stated by User
- **Bias** – Recipe database covers multiple dietary preferences and cuisines
- **Accuracy** – Recipes are simplified; users should verify cooking temps/times
- **Limitations** – No nutritional info, allergy warnings, or real-time ingredient pricing
- **Future Improvements** – Add allergen flags, dietary customization, nutritional data

---

## 🤖 Responsible AI Use

We used AI assistants to help plan this project and write starter text and code in plain beginner-friendly language.

### Our Responsibilities as the Students

- ✅ **We read and edited all generated content** to make sure we understand it
- ✅ **We ran the code and tests ourselves** to verify everything works
- ✅ **We fixed any mistakes or parts that may cause confusion or lack clarity** that the AI generated
- ✅ **We wrote the final commit messages and pull request descriptions in our own words**
- ✅ **AI does not replace our learning or testing. It is a helper. We remain responsible for what we submit.**

---


## Risks and Limitations
| Risk | Impact | Likelihood | Mitigation |
|-----|--------|------------|------------|
| Hallucination from AI in regards to recipes | Medium | AI models are improving overall, but can be more definitive with the prompt | change the prompt in the AI portion |
| Allergy inducing recipe | High | Med-High | Clear warning labels to user / Allergy settings or filter saved for each user |
| Overwhelming noise for user | Medium | Medium | Increase recipe limiting parameters |
| Sub par results | High | High | Every user has differing culinary skills and can produce meals that are well considered unsatisfactory, which may discourage users, which may help to have a user input of culinary skills to cater to recipes |

## 🛠️ Future Enhancements

- [ ] **OpenAI Integration** – Richer answers to free-form questions
- [ ] **Conversation Logging** – Optional session history (`history.log`)
- [ ] **Favorite Recipes** – Save and retrieve user favorites (JSON file)
- [ ] **Allergen Support** – Mark recipes safe for common allergies
- [ ] **Nutritional Info** – Display calories, protein, carbs per recipe
- [ ] **API Mode** – Expose as REST API for web frontend
- [ ] **Multi-Language** – Localization for Spanish, French, Arabic, etc.
- [ ] User Skill Level Input - cater recipes to user's culinary skills.

---

## 📞 Support & Questions

For issues, feature requests, or feedback:
1. Check **[BACKLOG.md](BACKLOG.md)** for current sprint tasks
2. Open a GitHub Issue labeled with `question` or `feature-request`
3. Contact the project lead (Desiree) or team members

---

## 👥 Team

- **David** (🟢) – Repo setup, CLI framework, README v1.0
- **Katie** (🔴) – Recipe database, UI/output formatting, demo video
- **Desiree** (🔵) – Conversation flow, intent detection, architecture diagrams
- **Morgan** (🟡) – Testing, error handling, ethics & bias documentation

---

## 📝 License

This project is part of the AIEG F25 Capstone. All rights reserved.

**Last Updated:** December 9, 2025
