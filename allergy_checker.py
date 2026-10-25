
class AllergyChecker:
    def __init__(self, graph):
        self.graph = graph

    # Time Complexity: O(n + I)
    # Checks each allergen and collects foods containing it.
    def find_foods_with_any_allergen(self, allergens):
        allergens = self._normalize_list(allergens)
        unsafe_foods = set()

        for allergen in allergens:
            unsafe_foods.update(
                self.graph.get_foods_for_ingredient(allergen)
            )

        return unsafe_foods

    # Time Complexity: O(n + I + d)
    # Starts with the ingredient found in the fewest foods,
    # then keeps only foods containing every requested ingredient.
    def find_foods_with_all_ingredients(self, ingredients):
        ingredients = self._normalize_list(ingredients)

        if not ingredients:
            return set()

        ingredient_foods = []

        for ingredient in ingredients:
            foods = self.graph.get_foods_for_ingredient(ingredient)

            if not foods:
                return set()

            ingredient_foods.append(foods)

        ingredient_foods.sort(key=len)
        result = ingredient_foods[0].copy()

        for foods in ingredient_foods[1:]:
            result.intersection_update(foods)

            if not result:
                break

        return result

    # Time Complexity: O(n + I + F*k)
    # First finds foods containing all the ingredients,
    # then checks which ones have exactly that ingredient set.
    def find_foods_with_exact_ingredients(self, ingredients):
        ingredients = self._normalize_list(ingredients)

        if not ingredients:
            return set()

        candidates = self.find_foods_with_all_ingredients(
            ingredients
        )
        exact_foods = set()

        for food in candidates:
            food_ingredients = (
                self.graph.get_ingredients_for_food(food)
            )

            if food_ingredients == set(ingredients):
                exact_foods.add(food)

        return exact_foods

    # Time Complexity: O(n + F + I)
    # Gets all foods, removes the ones containing allergens,
    # and returns the remaining foods as candidates.
    def find_safe_candidates(self, allergens):
        allergens = self._normalize_list(allergens)

        all_foods = set(self.graph.hyperedges.keys())
        unsafe_foods = self.find_foods_with_any_allergen(allergens)

        return all_foods - unsafe_foods

    # Time Complexity: O(n + I + k)
    # Checks which requested ingredients are present in each
    # matching food and prepares a short explanation.
    def explain_food_matches(self, ingredients):
        ingredients = self._normalize_list(ingredients)
        matching_foods = self.find_foods_with_all_ingredients(
            ingredients
        )

        explanations = []

        for food in sorted(matching_foods):
            food_ingredients = (
                self.graph.get_ingredients_for_food(food)
            )
            matched = sorted(set(ingredients).intersection(
                food_ingredients
            ))

            explanations.append({
                "food": food,
                "found": bool(matched),
                "matches": matched,
                "message": (
                    "All requested ingredients are present."
                    if matched else "No requested ingredients found."
                )
            })

        return explanations

    # Time Complexity: O(n + I)
    # Finds foods containing any ingredient in the selected food,
    # then removes the selected food from the result.
    def find_foods_sharing_ingredients(self, food):
        food = self._normalize_name(food)
        ingredients = self.graph.get_ingredients_for_food(food)

        related_foods = set()

        for ingredient in ingredients:
            related_foods.update(
                self.graph.get_foods_for_ingredient(ingredient)
            )

        related_foods.discard(food)
        return related_foods

    # Time Complexity: O(n + F + I)
    # Separates foods into safe and unsafe groups and reports
    # the counts and percentage of foods marked as safe.
    def get_safety_audit_report(self, allergens):
        allergens = self._normalize_list(allergens)

        all_foods = set(self.graph.hyperedges.keys())
        unsafe_foods = self.find_foods_with_any_allergen(allergens)
        safe_foods = all_foods - unsafe_foods

        total_foods = len(all_foods)

        if total_foods == 0:
            safe_percentage = 0
        else:
            safe_percentage = round(
                len(safe_foods) / total_foods * 100, 2
            )

        return {
            "total_foods": total_foods,
            "safe_foods": len(safe_foods),
            "unsafe_foods": len(unsafe_foods),
            "safe_percentage": safe_percentage,
            "allergens_checked": allergens,
            "safe_food_list": sorted(safe_foods),
            "unsafe_food_list": sorted(unsafe_foods)
        }

    # Time Complexity: O(n)
    # Removes extra spaces and makes the name lowercase.
    @staticmethod
    def _normalize_name(name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")

        name = name.strip().casefold()

        if not name:
            raise ValueError("Name cannot be empty.")

        return name

    # Time Complexity: O(n)
    # Cleans each name and removes duplicate ingredients.
    @classmethod
    def _normalize_list(cls, items):
        if isinstance(items, str):
            items = [items]

        try:
            items = list(items)
        except TypeError:
            raise TypeError("Expected a string or an iterable of names.")

        normalized = set()

        for item in items:
            normalized.add(cls._normalize_name(item))

        return normalized
