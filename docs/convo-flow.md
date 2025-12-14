Python main.py

CLI initialization followed up with
- meal_type
- diet_restrictions
-  greater than or > = 3 ingredients

parameters ran through logic and hard coded json file with recipes
- looks for 2 or more ingredient matches for recipe suggestions
- groq api fed parameters in prompt form to generate additional recipes
- within timeout length

return output to user in form of 5 choices of recipes
- can pick wih user input integer
- can ask for 'substitutions' within recipe
- user chooses a recipe, or can exit program

recipe is chosen
- step by step instructions listed
- macros
- cost of additional ingredients
- time for prep and creation

Exit
