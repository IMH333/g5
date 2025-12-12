# Recipe Suggestion Helper - OpenAI Enhanced ✨

Your Recipe Suggestion Helper is now **fully configured** to work with OpenAI for intelligent recipe generation!

## ✅ What's Working

1. **Environment Setup**
   - ✓ OpenAI API key loaded from `.env`
   - ✓ Python dependencies installed (`rich`, `openai`, `python-dotenv`)
   - ✓ Error handling and timeouts configured

2. **Features**
   - ✓ Local recipe matching from 9,921 recipes in `recipes.json`
   - ✓ AI-powered recipe generation when local matches are insufficient
   - ✓ Automatic fallback to AI when `< --max-results` local matches found
   - ✓ Dietary preference filtering (vegan, vegetarian, halal, kosher, etc.)
   - ✓ Meal type filtering (breakfast, lunch, dinner, snack)
   - ✓ Allergen warnings and nutrition estimates
   - ✓ Recipe saving and printable cards
   - ✓ Ingredient substitution suggestions
   - ✓ Interactive Q&A about recipes

## 🚀 How to Use

### Basic Usage
```bash
python main.py
```
Follow the prompts to enter:
- Meal type (optional)
- Dietary preferences (optional)
- Your available ingredients

### Advanced Options
```bash
# Show up to 6 recipe options (auto-generates with AI if needed)
python main.py --max-results=6

# Disable AI generation (local recipes only)
python main.py --no-ai

# Verify API key is loaded (shows masked key)
python main.py --show-key
```

## 🎯 Example Flow

```
Hi! I'm your Recipe Suggestion Helper.

Available meal types: breakfast, snack, lunch, dinner
What type of meal is this? (or press Enter to skip)
> dinner

Available dietary options: halal, kosher, pescatarian, vegan, vegetarian
Do you have any dietary preferences? (or press Enter to skip)
> vegan

Tell me what ingredients you have (comma-separated). Example: 'chicken, rice, broccoli'
What ingredients do you have?
> tofu, rice, broccoli, soy sauce

Generating 3 more recipe(s)...
✓ Generated 5 recipe(s)

Great! Here are up to 8 recipe options:
1. Tofu Stir-Fry (20 minutes) — vegan [local] — matches 4 ingredient(s)
2. Rice Bowl with Tofu (25 minutes) — vegan [local] — matches 4 ingredient(s)
3. AI-Generated Tofu Bowl (15 minutes) — vegan 
4. Crispy Tofu & Broccoli (20 minutes) — vegan 
5. Asian Tofu Rice (25 minutes) — vegan 
...
```

## 🔧 Configuration

### Environment Variables (`.env`)
```bash
OPENAI_API_KEY=sk-proj-...your-key...
```

### Command Line Flags
- `--max-results=N` or `--max=N`: Show up to N recipes (default: 5)
- `--no-ai`: Disable AI generation, show local matches only
- `--show-key`: Display masked API key to verify it's loaded

## 🎨 Features Details

### AI Recipe Generation
- Automatically triggered when local matches < requested max results
- Generates 3-5 complete recipes with:
  - Title and estimated cooking time
  - Full ingredient lists
  - Step-by-step instructions
  - Dietary tags (vegan, vegetarian, halal, etc.)
  - Allergen warnings
  - Nutrition estimates (calories, protein, carbs, fat)

### Interactive Q&A
After selecting a recipe, you can:
- Ask about cooking time
- Request ingredient substitutions
- Ask "want to make this" to:
  - See shopping list (missing ingredients marked)
  - Get cost estimates
  - Save recipe to `saved_recipes.json`
  - Generate printable recipe card in `saved_cards/`
  - Get suggested prep/cook timers

### Smart Features
- Ingredient matching supports partial matches (e.g., "soba" matches "soba noodles")
- Rich terminal formatting with colors and emojis
- Best-effort allergen detection
- Rough nutrition estimates (not for medical use)

## 📝 Files

- `main.py` - Main CLI application
- `src/recipe_helper.py` - Recipe matching and local database logic
- `src/openai_helper.py` - OpenAI integration for AI generation
- `recipes.json` - Local recipe database (9,921 recipes)
- `saved_recipes.json` - Your saved recipes
- `saved_cards/` - Printable recipe cards
- `.env` - Your OpenAI API key (not committed to git)

## 🧪 Testing

Run the test script to verify everything works:
```bash
python test_app.py
```

This will:
1. Verify API key is loaded
2. Generate test recipes with OpenAI
3. Display results

## 🎉 Ready to Go!

Your app is now **working perfectly** with OpenAI integration. Just run:

```bash
python main.py
```

Enjoy cooking! 👨‍🍳👩‍🍳
