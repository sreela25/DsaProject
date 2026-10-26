class AllergyChecker:
    def __init__(self, graph):
        self.graph = graph
    # Finds foods containing at least one listed allergen.
    # Time: Proportional to the incidence sets visited and copied.
    def find_foods_with_any_allergen(self, allergens):
        allergens = self._normalize_list(allergens)
        unsafe = set()

        for allergen in allergens:
            unsafe.update(self.graph.get_foods_for_ingredient(allergen))
        return unsafe

    # Finds foods containing every requested ingredient.
    # Starts with the ingredient found in the fewest foods.
    # Time: Depends on the sizes of the incidence sets.
    def find_foods_with_all_ingredients(self, ingredients):
        ingredients = self._normalize_list(ingredients)
        if not ingredients:
            return set()

        sets = []
        for ingredient in ingredients:
            foods = self.graph.get_foods_for_ingredient(ingredient)
            if not foods:
                return set()
            sets.append(foods)

        sets.sort(key=len)
        result = sets[0].copy()

        for foods in sets[1:]:
            result.intersection_update(foods)
            if not result:
                break
        return result

    # Finds foods whose ingredient set exactly matches the requested set.
    # Time: Depends on candidate count and the ingredients in each candidate.
    def find_foods_with_exact_ingredients(self, ingredients):
        requested = self._normalize_list(ingredients)
        if not requested:
            return set()

        candidates = self.find_foods_with_all_ingredients(requested)
        return {
            food for food in candidates
            if self.graph.get_ingredients_for_food(food) == requested
        }

    # Finds foods with no recorded matches for the listed allergens.
    # Time: O(F + I) in the general case.
    def find_safe_candidates(self, allergens):
        all_foods = set(self.graph.hyperedges)
        unsafe = self.find_foods_with_any_allergen(allergens)
        return all_foods - unsafe

    # Explains which foods contain all requested ingredients.
    # Time: Depends on the matching search and the returned food ingredients.
    def explain_food_matches(self, ingredients):
        requested = self._normalize_list(ingredients)
        matching_foods = self.find_foods_with_all_ingredients(requested)
        reports = []

        for food in sorted(matching_foods):
            actual = self.graph.get_ingredients_for_food(food)
            matched = sorted(requested & actual)
            reports.append({
                "food": food,
                "found": bool(matched),
                "matches": matched,
                "message": "All requested ingredients are present."
            })

        return reports

    # Finds other foods sharing one or more ingredients with the selected food.
    # Time: Depends on the incidence sets visited.
    def find_foods_sharing_ingredients(self, food):
        food = self.graph._normalize_name(food)
        ingredients = self.graph.get_ingredients_for_food(food)
        related = set()

        for ingredient in ingredients:
            related.update(self.graph.get_foods_for_ingredient(ingredient))

        related.discard(food)
        return related

    # Creates a summary of foods with and without recorded allergen matches.
    # Time: O(F + I) in the general case.
    def get_safety_audit_report(self, allergens):
        allergens = self._normalize_list(allergens)
        all_foods = set(self.graph.hyperedges)
        unsafe = self.find_foods_with_any_allergen(allergens)
        safe = all_foods - unsafe
        total = len(all_foods)

        percentage = round(len(safe) / total * 100, 2) if total else 0

        return {
            "total_foods": total,
            "safe_foods": len(safe),
            "unsafe_foods": len(unsafe),
            "safe_percentage": percentage,
            "allergens_checked": sorted(allergens),
            "safe_food_list": sorted(safe),
            "unsafe_food_list": sorted(unsafe)
        }

    # Cleans and validates one name.
    # Time: O(n), where n is the name length.
    @staticmethod
    def _normalize_name(name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        name = name.strip().casefold()
        if not name:
            raise ValueError("Name cannot be empty.")
        return name

    # Cleans names and removes duplicates.
    # Time: Proportional to the total length of the input names.
    @classmethod
    def _normalize_list(cls, items):
        if isinstance(items, str):
            items = [items]

        try:
            items = list(items)
        except TypeError:
            raise TypeError("Expected a string or an iterable of names.")

        return {cls._normalize_name(item) for item in items}
