class HyperGraph:
    """Stores ingredients as vertices and foods as hyperedges."""

    def __init__(self):
        self.vertices = set()
        self.hyperedges = {}
        self.incidence = {}

    # Adds an ingredient if it is not already present.
    # Time: O(n) for name cleanup; set/dictionary operations are O(1) average.
    def add_ingredient(self, ingredient):
        ingredient = self._normalize_name(ingredient)
        if ingredient in self.vertices:
            return False
        self.vertices.add(ingredient)
        self.incidence[ingredient] = set()
        return True

    # Deletes one ingredient vertex and all its links.
    # Foods left with no ingredients are deleted as well.
    # Time: O(n + d), where d is the number of foods using this ingredient.
    def delete_vertex(self, ingredient):
        ingredient = self._normalize_name(ingredient)
        if ingredient not in self.vertices:
            return False

        affected_foods = list(self.incidence[ingredient])

        for food in affected_foods:
            self.hyperedges[food].discard(ingredient)
            if not self.hyperedges[food]:
                del self.hyperedges[food]
                for other_ingredient in list(self.incidence):
                    self.incidence[other_ingredient].discard(food)

        del self.incidence[ingredient]
        self.vertices.remove(ingredient)
        return True

    # Adds a food or replaces the ingredients of an existing food.
    # Time: O(k_old + k_new), excluding the cost of processing name characters.
    def add_food(self, food, ingredients):
        food = self._normalize_name(food)

        if isinstance(ingredients, str):
            raise TypeError("Enter ingredients as a list.")

        try:
            ingredients = list(ingredients)
        except TypeError:
            raise TypeError("Ingredients must be iterable.")

        if not ingredients:
            raise ValueError("A food must have at least one ingredient.")

        ingredients = {self._normalize_name(item) for item in ingredients}

        for ingredient in ingredients:
            self.add_ingredient(ingredient)

        if food in self.hyperedges:
            for old_ingredient in self.hyperedges[food]:
                self.incidence[old_ingredient].discard(food)

        self.hyperedges[food] = ingredients
        for ingredient in ingredients:
            self.incidence[ingredient].add(food)
        return True

    # Removes a food hyperedge and its links.
    # Time: O(k), where k is the number of ingredients in the food.
    def remove_food(self, food):
        food = self._normalize_name(food)
        if food not in self.hyperedges:
            return False

        ingredients = self.hyperedges.pop(food)
        for ingredient in ingredients:
            self.incidence[ingredient].discard(food)
        return True

    # Checks whether a food exists.
    # Time: O(n) for name cleanup, then O(1) average lookup.
    def contains_food(self, food):
        return self._normalize_name(food) in self.hyperedges

    # Returns foods linked to an ingredient.
    # Time: O(n + d), including copying the result set.
    def get_foods_for_ingredient(self, ingredient):
        ingredient = self._normalize_name(ingredient)
        return set(self.incidence.get(ingredient, set()))

    # Returns ingredients linked to a food.
    # Time: O(n + k), including copying the result set.
    def get_ingredients_for_food(self, food):
        food = self._normalize_name(food)
        return set(self.hyperedges.get(food, set()))

    # Finds foods containing both ingredients.
    # Time: O(min(d1, d2)) average, after name cleanup.
    def get_common_foods(self, ingredient1, ingredient2):
        ingredient1 = self._normalize_name(ingredient1)
        ingredient2 = self._normalize_name(ingredient2)

        foods1 = self.incidence.get(ingredient1, set())
        foods2 = self.incidence.get(ingredient2, set())

        if len(foods1) > len(foods2):
            foods1, foods2 = foods2, foods1

        return {food for food in foods1 if food in foods2}

    # Counts foods containing an ingredient.
    # Time: O(n) for name cleanup; set length is O(1).
    def count_foods_for_ingredient(self, ingredient):
        ingredient = self._normalize_name(ingredient)
        return len(self.incidence.get(ingredient, set()))

    # Time: O(1).
    def get_vertex_count(self):
        return len(self.vertices)

    # Time: O(1).
    def get_hyperedge_count(self):
        return len(self.hyperedges)

    # Counts all ingredient-food links.
    # Time: O(F), where F is the number of foods.
    def get_incidence_count(self):
        return sum(len(ingredients) for ingredients in self.hyperedges.values())

    # Prints every food and its ingredients.
    # Time: O(F log F + sum(k log k)) due to sorting.
    def display_hypergraph(self):
        print("\n========== FOOD HYPERGRAPH ==========")
        if not self.hyperedges:
            print("No foods available.")
            return

        for food in sorted(self.hyperedges):
            print(food.title(), "->", ", ".join(sorted(self.hyperedges[food])))
        print("=" * 38)

    # Prints the reverse ingredient-to-food index.
    # Time: Depends on sorting the ingredient and food names.
    def display_incidence_index(self):
        print("\n========== INCIDENCE INDEX ==========")
        if not self.incidence:
            print("No ingredients available.")
            return

        for ingredient in sorted(self.incidence):
            foods = sorted(self.incidence[ingredient])
            food_names = ", ".join(food.title() for food in foods) if foods else "No foods"
            print(f"{ingredient.title():<15} -> {food_names} ({len(foods)} foods)")
        print("=" * 38)

    # Shows graph counts and checks that both indexes agree.
    # Time: O(V + F + I).
    def display_statistics(self):
        print("\n========== HYPERGRAPH STATISTICS ==========")
        print("Ingredient vertices:", self.get_vertex_count())
        print("Food hyperedges:", self.get_hyperedge_count())
        print("Ingredient-food links:", self.get_incidence_count())
        print("Valid structure:", self.validate_invariants())
        print("=" * 42)

    # Cleans a name before using it as a key.
    # Time: O(n), where n is the name length.
    @staticmethod
    def _normalize_name(name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        name = name.strip().casefold()
        if not name:
            raise ValueError("Name cannot be empty.")
        return name

    # Checks that hyperedges and the incidence index match.
    # Time: O(V + F + I), using average-case set/dictionary operations.
    def validate_invariants(self):
        if any(not ingredients.issubset(self.vertices)
               for ingredients in self.hyperedges.values()):
            return False

        expected = {ingredient: set() for ingredient in self.vertices}
        for food, ingredients in self.hyperedges.items():
            for ingredient in ingredients:
                expected[ingredient].add(food)
        return expected == self.incidence


if __name__ == "__main__":
    graph = HyperGraph()
    graph.add_food("Pizza", ["Wheat", "Milk", "Cheese", "Tomato"])
    graph.add_food("Pasta", ["Wheat", "Egg", "Cheese", "Tomato"])
    graph.add_food("Cake", ["Wheat", "Egg", "Milk", "Butter"])
    graph.display_hypergraph()
    graph.display_incidence_index()
    graph.display_statistics()
