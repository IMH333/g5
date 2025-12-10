# Ethics & Responsibility – Recipe Suggestion Helper

## 🔒 Privacy

### Data Collection & Storage
- **No user data is logged or stored** by default
- Each conversation session is **ephemeral** (exists only in memory during runtime)
- Users are never prompted for personal information (name, email, location, etc.)
- No analytics, telemetry, or cookies

### Future Considerations
If we add optional logging (e.g., `history.log`):
- Users must explicitly opt-in
- Log files should be stored locally on the user's machine only
- Include a clear privacy notice in the CLI
- Provide option to delete logs: `--clear-history` flag

### OpenAI Integration (Optional)
If OpenAI API is enabled (via `OPENAI_API_KEY`):
- API calls include the recipe context and user questions
- Review OpenAI's [privacy policy](https://openai.com/privacy/)
- Consider if this meets your data governance needs
- **Recommendation:** Disable in environments handling sensitive dietary info

---

## 🚨 Potential Biases

### Database Representation
**Current state:**
- ✅ 13 recipes covering diverse cuisines and dietary preferences..along with massive database of 100 recipes
- ✅ Halal, Kosher, Vegan, Vegetarian, Pescatarian options
- ✅ Mix of global cuisines (Asian, Italian, Indian, Middle Eastern)
- ⚠️ Could add more African, Latin American, and Middle Eastern recipes

**What we did to mitigate:**
- Explicitly support 5 dietary categories (not just Western vegetarian)
- Include substitution suggestions for common ingredient swaps (culturally respectful)
- No weight toward any single cuisine

**Future improvements:**
- Add 5–10 more recipes from underrepresented cuisines
- Include regional variations (e.g., multiple dal recipes, taco variants)
- User survey to identify missing recipe types

### Ingredient Normalization
**Risk:** Spelling variations or regional names might not match
- "Tofu" vs "Bean curd"
- "Cilantro" vs "Coriander"
- "Chickpea" vs "Garbanzo"

**Mitigation:**
- Keep ingredient list in recipes.json in simple, common English terms
- Consider adding aliases in future versions

### Dietary Labels
**Risk:** Misrepresenting recipes as suitable for a diet
- "Vegetarian" is well-defined (no meat)
- "Halal" has strict Islamic rules (our simplified version may not be fully halal)
- "Kosher" similarly has complex rules we oversimplify

**Mitigation:**
- Add disclaimer: "Recipes marked as halal/kosher are simplified suggestions. Verify with community standards."
- Suggest users consult certified sources for strict compliance

---

## ⚠️ Limitations & Risk Assessment

### Accuracy Issues
| Risk | Impact | Mitigation |
|------|--------|-----------|
| Recipes are simplified; don't include all details | User might burn food or get poor results | Include step count and time estimates; suggest consulting full recipes online |
| No nutritional information provided | Users with dietary needs (diabetes, allergies) can't make informed decisions | Recommend consulting nutrition databases (USDA, MyFitnessPal) for detailed data |
| No allergy warnings (nuts, dairy, shellfish, etc.) | Severe allergic reactions possible | Add clear disclaimer: "Not a substitute for allergy information. Verify ingredients." |
| Cooking temperatures/times are generic | Food safety issues (undercooked poultry, fish) | Include reminder: "Use a food thermometer. Verify doneness." |
| Ingredients listed without sourcing info | Ingredients may have hidden animal products or processing concerns | Add note: "Verify ingredient sourcing matches your dietary values." |

### Functional Limitations
- No real-time ingredient pricing (cost estimates not available)
- No inventory management (can't track what user actually has)
- No nutrition calculator (can't suggest low-calorie or high-protein options)
- Ingredient matching is case-insensitive but not fuzzy (typos won't match)
- Limited to 13 pre-loaded recipes (not a comprehensive recipe database)

### Conversation Limitations
- Intent detection is rule-based (regex + keywords), not ML-powered
- Free-form questions only work if they match predefined patterns
- No natural language understanding of nuance or context
- Substitution suggestions are hard-coded (limited to 8 suggestions)
- Can't learn from user feedback or adapt over time

---

## 🌍 Broader Ethical Considerations

### Food Security & Equity
- **Risk:** Bot recommends recipes that assume access to ingredients (fresh produce, diverse proteins)
- **Reality:** Not everyone can afford or access all ingredients
- **Mitigation:** Focus on recipes using pantry staples + seasonal ingredients. Add "budget-friendly" tag in future.

### Cultural Sensitivity
- **Risk:** Oversimplifying recipes from cultures we don't deeply understand
- **Reality:** Our team may not have expertise in all cuisines represented
- **Mitigation:**
  - Credit sources for recipes (e.g., "Inspired by traditional Indian cuisine")
  - Invite community feedback on recipes
  - Partner with cultural consultants if expanding

### Misinformation & AI Hype
- **Risk:** Users think the bot understands nutrition, allergies, or cooking science
- **Reality:** It's a simple rule-based system with no medical/nutritional training
- **Mitigation:**
  - Disclaimers throughout ("not a nutritionist," "verify ingredients," "consult thermometer")
  - Be transparent about limitations in README and demo
  - Don't claim the bot is "smart" or "learns"—call it what it is: a suggestion engine

### Labor & Attribution
- **Risk:** Recipes sourced from online without clear attribution
- **Reality:** Many recipes online lack clear copyright info
- **Mitigation:**
  - Document where each recipe came from (comment in recipes.json)
  - Mark recipes as "inspired by" rather than "copied from"
  - Link to original sources where available

---

## 🤖 Responsible AI Use

We used AI assistants to help plan this project and write starter text and code in plain beginner-friendly language.

### Our Responsibilities as the Students

- ✅ **We read and edited all generated content** to make sure we understand it
- ✅ **We ran the code and tests ourselves** to verify everything works
- ✅ **We fixed any mistakes or confusing parts** that the AI generated
- ✅ **We wrote the final commit messages and pull request descriptions in our own words**
- ✅ **We remain responsible for what we submit**

### Why This Matters

AI does not replace our learning or testing. It is a helper. We use it to accelerate development while maintaining full accountability for the final product. Every feature, function, and decision in this codebase has been reviewed, tested, and understood by our team.

---

## 🔮 Future Enhancements (Responsible Expansion)

### Phase 1: Safety & Accuracy (High Priority)
- [ ] Add allergy warning flags (nuts, dairy, shellfish, etc.)
- [ ] Include cooking temperature targets (FDA/USDA standards)
- [ ] Add disclaimer modal on startup
- [ ] Expand ingredient list to 20+ recipes

### Phase 2: Inclusivity (Medium Priority)
- [ ] Add more cuisines (African, Latin American, Southeast Asian)
- [ ] "Budget-friendly" recipes using minimal ingredients
- [ ] Accessibility: Text-to-speech for recipe steps
- [ ] Multi-language support (Spanish, Arabic, Mandarin)

### Phase 3: Capability (Lower Priority, if time allows)
- [ ] OpenAI integration for richer Q&A
- [ ] Nutritional calculator (API integration)
- [ ] User preference saving (no personal data, just recipe favorites)
- [ ] Session logging with user consent

---

## 📋 Compliance & Standards

### Data Protection
- ✅ **GDPR compliant** (no personal data collected)
- ✅ **CCPA compliant** (no data to disclose or delete)
- ⚠️ **Future:** If logging added, must comply with local privacy laws

### Accessibility
- ✅ Text-based CLI (works with screen readers)
- ⚠️ No color-coding of output (could help colorblind users)
- ⚠️ Could add `--verbose` mode with more descriptive steps

### Safety & Responsibility
- ✅ No toxic language or inappropriate content
- ✅ No profiling or discrimination
- ⚠️ Could add content policy for user-generated data (if added later)

---

## 🤝 Responsible AI Principles

Our project follows these principles:

1. **Transparency** – Clear about what the bot can and can't do
2. **Accountability** – Team documented design decisions and tradeoffs
3. **Fairness** – Recipes represent diverse diets and cultures
4. **Privacy** – No user data collection by default
5. **Safety** – Disclaimers for food safety concerns
6. **Respect** – Credit sources; acknowledge limitations

---

## 📞 Reporting Concerns

If you identify a bias, safety issue, or privacy concern:
1. Open a **GitHub Issue** with label `ethics` or `safety`
2. Contact the project lead (Desiree) privately
3. Include:
   - Description of the issue
   - Impact (who is affected?)
   - Suggested mitigation

---

## 👥 Acknowledgments

This ethics document was developed by **Morgan (🟡)** as part of the team's commitment to responsible AI. We welcome feedback and improvements.

---

**Last Updated:** December 9, 2025

**Next Review:** After first user feedback cycle or quarterly, whichever comes first
