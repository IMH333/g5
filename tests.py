import unittest


def safe_default(ingredients):
    if len(ingredients) < 3:
        return "Go grocery shopping"
    return None


class TestSafeDefault(unittest.TestCase):

    def test_less_than_three_ingredients(self):
        result = safe_default(["apple", "milk"])
        self.assertEqual(result, "Go grocery shopping")


def validate_ingredients(raw_input):
    # user types: "apple,   milk,  , bread"
    return [i.strip() for i in raw_input.split(",") if i.strip()]


class TestValidateIngredients(unittest.TestCase):

    def test_validation_removes_empty_and_strips(self):
        result = validate_ingredients("apple,  milk , , bread  ")
        self.assertEqual(result, ["apple", "milk", "bread"])


if __name__ == "__main__":
    unittest.main()
