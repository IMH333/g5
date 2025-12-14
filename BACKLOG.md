# Sprint Backlog – Recipe Suggestion Helper (CLI AI Chatbot)
**Project:** AIEG F25 Capstone  
**Sprint Goal:** Deliver a fully working CLI chatbot by Dec 12 that:
- Takes user ingredients → suggests 2–3 matching recipes from JSON
- Uses OpenAI/Claude for natural follow-up questions
- Feels smooth and natural in the terminal

**Team Legend**  
🔵 Desiree | 🔴 Katie | 🟢 David | 🟡 Morgan  

| #  | Task (1–2 days)                                      | Owner   | Status       | GitHub Issue |
|----|-------------------------------------------------------|---------|--------------|--------------|
| 1  | Create GitHub repo + initial README + .gitignore      | 🟢 David | ✅ Done     | —            |
| 2  | Set up Python venv + dependencies (openai/anthropic, dotenv, rich/click) | 🔵 Desiree | ⏳ In Progress | —            |
| 3  | Build basic CLI loop (welcome → input → response → repeat/exit) | 🔵 Desiree | ⏳         |              |
| 4  | Create `recipes.json` with ~12 common recipes (title, ingredients, steps, tags) | 🔴 Katie | ⏳          |              |
| 5  | Write recipe matcher (user must have ≥2 required ingredients) | 🔴 Katie | ⏳          |              |
| 6  | Pretty-print 2–3 recipe suggestions in terminal (Rich tables or cards) | 🔴 Katie | ⏳          |              |
| 7  | Design conversation flow diagram            | 🟢 David | ✅ Done           |              |
| 8  | Implement intent detection (regex + keywords)         | 🟢 David | ✅ Done           |              |
| 9  | Write system prompt + few-shot examples for natural follow-ups | 🟢 David | ✅ Done 
|10  | Integrate OpenAI API calls with error handling & timeouts | 🟢 David | ✅ Done           |              |
|11  | Add session memory (store user ingredients + selected recipe) | 🟡 Morgan | ⏳          |              |
|12  | Handle “I don’t have X” → use AI to modify/substitute ingredients | 🟡 Morgan | ⏳          |              |
|13  | Graceful error handling + friendly fallback messages | 🟡 Morgan | ⏳          |              |
|14  | Write 25+ manual test cases (happy/path + edge cases) | 🟡 Morgan | ⏳          |              |
|15  | Create final architecture + conversation flow diagrams (for README) | 🟢 David | ⏳          |              |
|16  | Record 2–3 min demo video + prep showcase slides (everyone speaks) | 🔴 Katie (lead) | ⏳   |              |
|17  | Polish README v1.0 (Quickstart, diagrams, limitations) | 🔵 Desiree | ⏳         |              |
|18  | Write Ethics & Bias doc (hallucinations, dietary accuracy, privacy) | 🟡 Morgan | ⏳         |              |

### Stretch Goals (if time)
- [ ] Log conversations to `history.log`
- [ ] Add dietary filters (vegan, gluten-free, keto flags in JSON)
- [ ] Save favorite recipes to a simple JSON file

### How to Use This Backlog in GitHub
1. Turn each row into a GitHub Issue → assign the owner + label (e.g., `backend`, `prompt`, `ui`, `qa`)
2. Or import directly into **GitHub Projects (beta)** as a table view
3. Drag tasks into To Do → In Progress → Done as you go!

Last updated: December 08, 2025  
(We’ll keep this file current — commit after every stand-up!)
