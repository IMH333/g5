# Demo Walkthrough – Recipe Suggestion Helper

## 🎬 Demo Flow (4–6 Minutes)

### Scene 1: Initial Setup & Greeting (30 sec)
**What to show:**
- Start terminal
- Run `python main.py`
- Bot greets user and lists available dietary options

**Bot output:**
```
Hi! I'm your Recipe Suggestion Helper.
Available dietary options: halal, kosher, pescatarian, vegan, vegetarian
Do you have any dietary preferences? (or press Enter to skip)
```

**Talking point:** "The bot supports five dietary preferences. Users can skip this if they don't have restrictions."

---

### Scene 2: Vegan Diet + Ingredients (1 min)

**User input:**
```
> vegan
> tofu, broccoli, garlic, soy sauce
```

**Bot response:**
```
Great! Here are some recipes you can make:
1. Tofu Stir-Fry (20 minutes) — vegan, vegetarian — matches 4 ingredient(s)
2. Lentil & Vegetable Curry (30 minutes) — vegan, vegetarian — matches 2 ingredient(s)
3. Quick Veggie Stir-Fry (15 minutes) — vegan, vegetarian, halal, kosher — matches 3 ingredient(s)

Which number would you like to know more about, or type a recipe name? (or 'no' to exit)
```

**User selects:**
```
> 1
```

**Bot shows recipe:**
```
Tofu Stir-Fry (20 minutes)
Dietary tags: vegan, vegetarian

- Step 1: Press tofu and cut into cubes.
- Step 2: Pan-fry tofu until golden, set aside.
- Step 3: Stir-fry veggies and garlic, add tofu back with soy sauce, cook until done.
```

**Talking point (Katie):** "We collected 13 recipes in a JSON database. Each recipe includes ingredients, time, dietary tags, and step-by-step instructions. The UI formats them nicely using simple text tables."

---

### Scene 3: Answer Follow-Up Questions (1 min)

**User asks about time:**
```
> How long does it take?
This recipe takes about 20 minutes
```

**User asks about substitution:**
```
> Can I substitute soy sauce?
I don't have a good substitute suggestion for that.
```

**User asks about butter:**
```
> I don't have butter, what can I use?
You can try: oil
```

**Talking point (David):** "We built simple intent detection using regex and keyword matching. The bot recognizes questions about time, substitutions, and steps. For richer answers, we can plug in OpenAI, but it works fully offline right now."

---

### Scene 4: Graceful Exit (30 sec)

**User exits:**
```
> exit
Bye — happy cooking!
```

**Talking point (Desiree):** "The conversation flow is natural—users always know what they can ask, and we handle edge cases like no matches or unrecognized input."

---

## 📊 Intent Classification Examples

### Intent 1: List Ingredients
**User input:** "I have chicken, rice, and broccoli"
- **Recognition:** Contains ingredient keywords
- **Action:** Parse and match against recipes
- **Response:** Show top 3 matching recipes

### Intent 2: Get Suggestions
**User input:** "What can I cook?"
- **Recognition:** Comes after ingredient input
- **Action:** Return matched recipes sorted by ingredient overlap
- **Response:** Numbered list with dietary tags

### Intent 3: Explain Recipe
**User input:** "Tell me about the stir-fry" or "1"
- **Recognition:** Recipe selection or title
- **Action:** Look up recipe and format steps
- **Response:** Full recipe with time and dietary info

### Intent 4: Ask Questions
**Subintent 4a – Time:**
- **Input:** "How long does it take?" / "What's the time?"
- **Response:** Return recipe time

**Subintent 4b – Substitution:**
- **Input:** "Can I use oil instead of butter?" / "I don't have X"
- **Response:** Suggest alternatives from substitution map

**Subintent 4c – Repeat Steps:**
- **Input:** "Show me the steps again" / "How do I make it?"
- **Response:** Re-display full recipe with steps

### Intent 5: Exit
**User input:** "exit" / "quit" / "no" / "goodbye"
- **Recognition:** Exit keywords
- **Action:** End session
- **Response:** Friendly goodbye

---

## 🛡️ Error Handling Examples

### Error 1: No Matching Recipes
**Scenario:** User has "banana, milk, flour" but selects Halal diet
```
Sorry, I couldn't find recipes matching at least 2 of your ingredients
with the 'halal' dietary requirement.
Try adding more ingredients or removing dietary filters.
```

### Error 2: Invalid Recipe Selection
**Scenario:** User enters "999" when only 3 recipes shown
```
Couldn't find that selection. Exiting.
```

### Error 3: Empty Input
**Scenario:** User hits Enter without typing ingredients
```
I didn't hear any ingredients. Exiting.
```

### Error 4: Unrecognized Question
**Scenario:** User asks "What's the weather?"
```
Sorry — I can answer substitution and time questions. 
For richer answers, set OPENAI_API_KEY and use the main project with OpenAI integration.
```

---

## 🔄 Conversation Examples by Diet

### Halal Example
```
> halal
> chicken, rice, oil, soy sauce
Great! Here are some recipes you can make:
1. Chicken & Rice Bowl (25 minutes) — halal, kosher
2. Chicken Stir-Fry (20 minutes) — halal, kosher
3. Quick Veggie Stir-Fry (15 minutes) — vegan, vegetarian, halal, kosher
> 1
[Shows Chicken & Rice Bowl recipe]
```

### Kosher Example
```
> kosher
> egg, milk, onion, bell pepper
Great! Here are some recipes you can make:
1. Veggie Omelette (10 minutes) — vegetarian, kosher
2. Lentil & Vegetable Curry (30 minutes) — vegan, vegetarian
[Note: Curry shows because 2+ ingredients match]
```

### Pescatarian Example
```
> pescatarian
> fish, lemon, olive oil
Great! Here are some recipes you can make:
1. Grilled Fish with Lemon (20 minutes) — pescatarian, halal, kosher
> 1
[Shows Grilled Fish with Lemon recipe]
> How long does it take?
This recipe takes about 20 minutes
```

### No Diet Filter (Most Options)
```
> [skip]
> tofu, rice, carrot, peas
Great! Here are some recipes you can make:
1. Tofu Stir-Fry (20 minutes) — vegan, vegetarian
2. Fried Rice (15 minutes) — vegetarian
3. Quick Veggie Stir-Fry (15 minutes) — vegan, vegetarian, halal, kosher
```

---

## 💡 Design Decisions & Talking Points

### Why 2-Ingredient Minimum?
"We set a minimum of 2 matching ingredients to ensure suggestions are actually relevant. A single match could be too vague."

### Why Dietary Filters Are Optional?
"Not everyone has dietary restrictions, and filtering can reduce options. We let users skip this to see everything available."

### Why JSON for Recipes?
"JSON is human-readable and easy to update. No database setup required. Perfect for a hackathon-style project."

### Why No API Key Required?
"We built the core logic to work offline. Users can test immediately without API setup. OpenAI integration is a future enhancement."

### Why Simple Substitutions Instead of AI?
"For a 4-6 minute demo, built-in substitutions are reliable. AI could hallucinate wrong advice. We opted for safety."

---

## 🎤 Team Talking Points

### Desiree (CLI & Architecture)
- Explains the conversation flow and user interaction loop
- Shows how `main.py` orchestrates the experience
- Talks about the project structure and modularity

### Katie (Recipes & UI)
- Presents the recipe database and dietary diversity
- Explains ingredient normalization and matching logic
- Shows output formatting and user-friendly messages

### David (Intent Detection & Design)
- Walks through the 4–5 intent types users can express
- Demonstrates how the bot recognizes each intent
- Explains the conversation flow diagram

### Morgan (Testing & Responsibility)
- Summarizes test cases (happy path + edge cases)
- Discusses error handling and graceful failures
- Presents the ethics & bias considerations (see ETHICS.md)

---

## ✅ Checklist for Demo Day

- [ ] Test `python main.py` on demo machine
- [ ] Pre-load 2–3 ingredient combinations to try
- [ ] Have alt diet preferences ready (vegan, halal, pescatarian)
- [ ] Show recipe details, time Q&A, and substitution flow
- [ ] Demonstrate graceful exit
- [ ] Each team member has 1–2 talking points ready
- [ ] Have ETHICS.md and README.md links available for Q&A
- [ ] Total demo time: 4–6 minutes max

---

