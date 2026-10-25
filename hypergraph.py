
class HyperGraph:
    """
    Food Ingredient Allergy Checker using a Hypergraph.

    Vertices: Ingredients
    Hyperedges: Foods connected to multiple ingredients
    Incidence index: Ingredient -> foods containing it

    V = number of ingredients
    F = number of foods
    I = total ingredient-food relationships
    k = ingredients in a food
    d = foods containing an ingredient
    """

    # Time Complexity: O(1)
    # Reason: Creates three empty data structures.
    def __init__(self):
        self.vertices = set()
        self.hyperedges = {}
        self.incidence = {}

    # Time Complexity: O(n)
    # Reason: Strips and converts the ingredient name.
    # Set and dictionary operations take O(1) average time.
    def add_ingredient(self, ingredient):
        ingredient = self._normalize_name(ingredient)

        if ingredient in self.vertices:
            return False

        self.vertices.add(ingredient)
        self.incidence[ingredient] = set()
        return True

    # Time Complexity: O(n + d)
    # Reason: Visits all foods containing the ingredient to remove the corresponding links.
    def remove_ingredient(self, ingredient):
        ingredient = self._normalize_name(ingredient)

        if ingredient not in self.vertices:
            return False

        for food in list(self.incidence[ingredient]):
            self.hyperedges[food].discard(ingredient)

        del self.incidence[ingredient]
        self.vertices.remove(ingredient)
        return True

    # Time Complexity: O(n + k) for a new food
    # Reason: Normalizes the names and adds k ingredient links.
    # Updating a food takes O(n + k_old + k_new), excluding the total character-processing cost of all names.
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

        ingredients = {
            self._normalize_name(item) for item in ingredients
        }

        for ingredient in ingredients:
            self.add_ingredient(ingredient)

        if food in self.hyperedges:
            for ingredient in self.hyperedges[food]:
                self.incidence[ingredient].discard(food)

        self.hyperedges[food] = ingredients

        for ingredient in ingredients:
            self.incidence[ingredient].add(food)

        return True

    # Time Complexity: O(n + k)
    # Reason: Removes the food and its k ingredient links.
    def remove_food(self, food):
        food = self._normalize_name(food)

        if food not in self.hyperedges:
            return False

        ingredients = self.hyperedges.pop(food)

        for ingredient in ingredients:
            self.incidence[ingredient].discard(food)

        return True

    # Time Complexity: O(n)
    # Reason: Name normalization takes O(n);
    # dictionary lookup takes O(1) average time.
    def contains_food(self, food):
        food = self._normalize_name(food)
        return food in self.hyperedges

    # Time Complexity: O(n + d)
    # Reason: Normalizes the ingredient and copies its d foods.
    def get_foods_for_ingredient(self, ingredient):
        ingredient = self._normalize_name(ingredient)

        if ingredient not in self.incidence:
            return set()

        return set(self.incidence[ingredient])

    # Time Complexity: O(n + k)
    # Reason: Normalizes the food name and copies k ingredients.
    def get_ingredients_for_food(self, food):
        food = self._normalize_name(food)

        if food not in self.hyperedges:
            return set()

        return set(self.hyperedges[food])

    # Time Complexity: O(n1 + n2 + min(d1, d2))
    # Reason: Normalizes both names, then iterates over the smaller incidence set and checks membership in the larger.
    def get_common_foods(self, ingredient1, ingredient2):
        ingredient1 = self._normalize_name(ingredient1)
        ingredient2 = self._normalize_name(ingredient2)

        if (ingredient1 not in self.incidence or
                ingredient2 not in self.incidence):
            return set()

        foods1 = self.incidence[ingredient1]
        foods2 = self.incidence[ingredient2]

        if len(foods1) > len(foods2):
            foods1, foods2 = foods2, foods1

        return {
            food for food in foods1
            if food in foods2
        }

    # Time Complexity: O(n)
    # Reason: Normalizes the name; set length is O(1).
    def count_foods_for_ingredient(self, ingredient):
        ingredient = self._normalize_name(ingredient)

        if ingredient not in self.incidence:
            return 0

        return len(self.incidence[ingredient])

    # Time Complexity: O(1)
    # Reason: Set length is stored and returned in constant time.
    def get_vertex_count(self):
        return len(self.vertices)

    # Time Complexity: O(1)
    # Reason: Dictionary length is returned in constant time.
    def get_hyperedge_count(self):
        return len(self.hyperedges)

    # Time Complexity: O(F)
    # Reason: Visits each food once to sum its ingredient count.
    def get_incidence_count(self):
        total = 0

        for ingredients in self.hyperedges.values():
            total += len(ingredients)

        return total

    # Time Complexity: O(F log F + I), plus ingredient sorting.
    # Reason: Sorts food names and each food's ingredient names.
    def display_hypergraph(self):
        print("\n========== FOOD HYPERGRAPH ==========")

        if not self.hyperedges:
            print("No foods available.")
            return

        for food in sorted(self.hyperedges):
            ingredients = sorted(self.hyperedges[food])
            print(food.title(), "->", ", ".join(ingredients))

        print("=" * 38)

    # Time Complexity: O(V log V + I), plus food-list sorting.
    # Reason: Sorts ingredients and the foods associated with them.
    def display_incidence_index(self):
        print("\n========== INCIDENCE INDEX ==========")

        if not self.incidence:
            print("No ingredients available.")
            return

        for ingredient in sorted(self.incidence):
            foods = sorted(self.incidence[ingredient])

            if foods:
                food_names = ", ".join(
                    food.title() for food in foods
                )
            else:
                food_names = "No foods"

            print(
                f"{ingredient.title():<15} -> "
                f"{food_names} ({len(foods)} foods)"
            )

        print("=" * 38)

    # Time Complexity: O(V + F + I)
    # Reason: Displays counts and validates the whole structure.
    def display_statistics(self):
        print("\n========== HYPERGRAPH STATISTICS ==========")
        print("Ingredient vertices:", self.get_vertex_count())
        print("Food hyperedges:", self.get_hyperedge_count())
        print("Ingredient-food links:", self.get_incidence_count())
        print("Valid structure:", self.validate_invariants())
        print("=" * 42)

    # Time Complexity: O(n)
    # Reason: Strips whitespace and normalizes the name.
    @staticmethod
    def _normalize_name(name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")

        name = name.strip().casefold()

        if not name:
            raise ValueError("Name cannot be empty.")

        return name

    # Time Complexity: O(V + F + I)
    # Reason: Checks hyperedges and rebuilds the incidence index.
    def validate_invariants(self):
        for ingredients in self.hyperedges.values():
            if not ingredients.issubset(self.vertices):
                return False

        expected = {
            ingredient: set()
            for ingredient in self.vertices
        }

        for food, ingredients in self.hyperedges.items():
            for ingredient in ingredients:
                expected[ingredient].add(food)

        return expected == self.incidence
