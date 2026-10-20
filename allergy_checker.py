
class AllergyChecker:
    def __init__(self, hypergraph):
        self.graph = hypergraph

    # 1. Find foods containing ANY of the given allergens.
    # Uses UNION of ingredient-to-food incidence sets.
    def find_foods_with_any_allergen(self, allergens):
        allergens = self._normalize_list(allergens)

        result = set()

        for allergen in allergens:
            result.update(
                self.graph.get_foods_for_ingredient(allergen)
            )

        return result

    # 2. Find foods containing ALL the specified ingredients.
    # Starts with the smallest incidence set to reduce work.
    def find_foods_with_all_ingredients(self, ingredients):
        ingredients = self._normalize_list(ingredients)

        if not ingredients:
            return set()

        ingredient_sets = []

        for ingredient in ingredients:
            foods = self.graph.get_foods_for_ingredient(ingredient)

            if not foods:
                return set()

            ingredient_sets.append(foods)

        ingredient_sets.sort(key=len)

        result = ingredient_sets[0].copy()

        for foods in ingredient_sets[1:]:
            result.intersection_update(foods)

            if not result:
                break

        return result

    # 3. Find foods whose recorded ingredient set matches exactly.
    def find_foods_with_exact_ingredients(self, ingredients):
        ingredients = set(self._normalize_list(ingredients))

        if not ingredients:
            return set()

        candidates = self.find_foods_with_all_ingredients(ingredients)

        result = set()

        for food in candidates:
            food_ingredients = self.graph.get_ingredients_for_food(food)

            if food_ingredients == ingredients:
                result.add(food)

        return result

    # 4. Find candidate foods that contain none of the listed allergens.
    # This is a recorded-data filter, not a guarantee of medical safety.
    def find_safe_candidates(self, allergens):
        allergens = self._normalize_list(allergens)

        all_foods = set(self.graph.hyperedges.keys())

        affected_foods = self.find_foods_with_any_allergen(allergens)

        return all_foods - affected_foods

    # 5. Explain which specified allergens are recorded in a food.
    def explain_food_matches(self, food, allergens):
        food = self._normalize_name(food)
        allergens = self._normalize_list(allergens)

        ingredients = self.graph.get_ingredients_for_food(food)

        if not ingredients:
            return {
                "food": food,
                "found": False,
                "matches": [],
                "message": "Food not found or has no recorded ingredients."
            }

        matches = sorted(ingredients.intersection(allergens))

        return {
            "food": food,
            "found": True,
            "matches": matches,
            "message": (
                "Recorded ingredient matches found."
                if matches
                else "No listed allergens found in the recorded ingredients."
            )
        }

    # 6. Find foods sharing at least one ingredient with a given food.
    def find_foods_sharing_ingredients(self, food):
        food = self._normalize_name(food)
        ingredients = self.graph.get_ingredients_for_food(food)

        if not ingredients:
            return set()

        result = set()

        for ingredient in ingredients:
            result.update(
                self.graph.get_foods_for_ingredient(ingredient)
            )

        result.discard(food)

        return result
        
    # 7. Generate a quick safety audit report for a user's allergies
    def get_safety_audit_report(self, allergens):
        all_foods = set(self.graph.hyperedges.keys())
        if not all_foods:
            return {"total_foods": 0, "safe_count": 0, "unsafe_count": 0, "safety_percentage": 0.0}

        unsafe_foods = self.find_foods_with_any_allergen(allergens)
        safe_foods = all_all_foods = all_foods - unsafe_foods if False else all_foods - unsafe_foods

        return {
            "total_foods": len(all_foods),
            "safe_count": len(safe_foods),
            "unsafe_count": len(unsafe_foods),
            "safety_percentage": round((len(safe_foods) / len(all_foods)) * 100, 2)
        }
        
    @staticmethod
    def _normalize_name(name):
        if not isinstance(name, str):
            raise TypeError("Names must be strings.")

        name = name.strip().casefold()

        if not name:
            raise ValueError("Names cannot be empty.")

        return name

    @classmethod
    def _normalize_list(cls, values):
        if isinstance(values, str):
            raise TypeError("Pass a collection of names, not one string.")

        normalized = set()

        for value in values:
            normalized.add(cls._normalize_name(value))

        return normalized
